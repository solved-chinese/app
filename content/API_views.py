import re

from dal import autocomplete
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from drf_spectacular.utils import extend_schema, OpenApiParameter, \
    OpenApiTypes, inline_serializer

from content.models import GeneralQuestion, LinkedField, Word, Sentence
from learning.models import Record
from content.utils import unaccent


class QuestionView(APIView):
    """
    get: Get question detail
    post: Check answer question answer
    """

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        question_pk = self.kwargs.pop('pk', None)
        self.question = get_object_or_404(GeneralQuestion.objects.all(),
                                          pk=question_pk)

    def get(self, request):
        show_all_options = request.session.get('show_all_options', False)
        try:
            client_dict = self.question.render(
                show_all_options=show_all_options
            )
        except ValidationError:
            raise NotFound
        return Response(client_dict)

    def post(self, request):
        data = request.data.copy()
        try:
            is_correct, correct_answer = self.question.check_answer(
                data.get('answer', None))
        except ValidationError:
            raise NotFound
        # create Record
        user = request.user if request.user.is_authenticated else None
        Record.objects.create(
            action=Record.Action.CORRECT_ANSWER if is_correct
                else Record.Action.WRONG_ANSWER,
            user=user,
            reviewable=self.question.reviewable,
            question=self.question,
            data={
                'answer': data.get('answer', None)
            }
        )
        return Response({
            'is_correct': is_correct,
            'answer': correct_answer,
        })


class LinkedFieldAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, result):
        if self.field_name == '__str__':
            field = str(self.field_name)
        else:
            field = getattr(result, self.field_name)
        return f"{repr(result)}'s {self.field_name}: {field}"

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_staff:
            return LinkedField.objects.none()

        content_type_id = self.forwarded.get('content_type', None)
        self.field_name = self.forwarded.get('field_name', '__str__')
        if content_type_id is None:
            return LinkedField.objects.none()

        model_class = ContentType.objects.get(pk=content_type_id).model_class()
        if model_class in (Word, Sentence):
            self.search_fields = ['chinese']
        else:
            return LinkedField.objects.none()

        if self.field_name in [field.name for field in Word._meta.fields]:
            self.search_fields.append(self.field_name)
        qs = model_class.objects.all()
        qs = self.get_search_results(qs, self.q)
        return qs


@extend_schema(
    parameters=[
        OpenApiParameter('keyword', OpenApiTypes.STR, required=True),
        OpenApiParameter(
            'query_type',
            OpenApiTypes.STR,
            default='auto',
            description="Must be 'auto', 'chinese', 'pinyin', or 'definition'"
        )
    ],
)
class SearchAPIView(APIView):
    """
    TODO documentation in progress

    searches keyword in content database

    keyword (str, required): the query keyword to be searched

    query_type (str, default=auto): should be among 'chinese', 'pinyin',
        'definition', 'auto'. This indicates what to search against in database.
        Use 'auto' to let the backend determine automatically.

    __returns__:

    results ([objects]): a list of serialized words / characters / radicals
    object (for now only supporting word results).

    query_type (str): 'chinese', 'pinyin', or 'definition', indicating what the
    backend uses for the search
    """
    def post(self, request):
        try:
            keyword = request.data['keyword']
        except KeyError:
            raise ParseError("keyword not found")
        query_type = request.data.get('query_type', 'auto').lower()
        if query_type not in ('auto', 'chinese', 'pinyin', 'definition'):
            raise ParseError(f"query type must be either 'auto', 'chinese',"
                             f" 'pinyin', or 'definition'. not {query_type}")

        keyword = keyword.strip()
        if not keyword:
            return Response({'results': [], 'query_type': 'definition'})

        if query_type in ('auto', 'chinese'):
            # searches for chinese words with keyword as substring
            chinese_regex = r'.*?'.join([''] + list(keyword) + [''])
            queryset = Word.objects.filter(chinese__regex=chinese_regex)
            if query_type == 'auto' and queryset.exists():
                query_type = 'chinese'
        if query_type in ('auto', 'pinyin'):
            # if problem with 儿化音, will use regex with many searchable
            # pinyin options
            pinyin_keyword = re.sub(r'[^a-zA-Z]', r'', unaccent(keyword))
            queryset = Word.objects.filter(
                searchable_pinyin__iexact=pinyin_keyword)
            if query_type == 'auto' and queryset.exists():
                query_type = 'pinyin'
        if query_type in ('auto', 'definition'):
            queryset = Word.objects.filter(
                definition__definition__search=keyword)
            query_type = 'definition'
        queryset = queryset.prefetch_related('definitions')
        results = [{
                'type': obj.__class__.__name__.lower(),
                'qid': obj.id,
                'chiense': obj.chinese,
                'pinyin': obj.pinyin,
                'definition': obj.full_definition,
            }
            for obj in queryset.all()
        ]
        return Response({
            'results': results,
            'query_type': query_type
        })

    POST_action = {
        'keyword': {
            'type': 'string',
            'example': 'hello',
        },
        'query_type': {
            'type': 'string',
            'example': 'auto',
        },
    }
