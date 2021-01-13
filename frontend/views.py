import re

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from content.models import WordSet


def temporary_access(request, access_id=1):
    wordset = get_object_or_404(WordSet, pk=access_id)
    request.session['temporary_access'] = wordset
    return HttpResponseRedirect(wordset.words.first().get_absolute_url())


def index(request):
    context = {}
    wordset = request.session.get('temporary_access', None)
    if wordset is not None:
        all_display = f'You can now preview set "{wordset.name}"<br>'
        words = wordset.words.filter(is_done=True).order_by('wordinset')
        if words.exists():
            pattern = r'^.*\/learning\/display\/\?t=word&qid=([0-9]+)$'
            match = re.match(pattern, request.build_absolute_uri())
            word_pk = int(match.group(1)) if match else -1
            all_display += ', '.join([
                '<a href="{}" {}>{}</a>'.format(
                    word.get_absolute_url(),
                    'style="color:red;"' if word_pk == word.pk else "",
                    word.chinese
                )
                for word in words
            ])
        else:
            all_display += "we are not prepared yet, come back later"
        context['temporary_access'] = all_display

    return render(request, 'learning/learning.html', context)