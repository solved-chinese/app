from django.db import transaction, models
from rest_framework import serializers, relations

from .models import Class, Teacher, Student, Assignment
from content.serializers import SimpleWordSerializer, SimpleCharacterSerializer, \
    RadicalSerializer
from content.models import Word, Character, Radical


class OrderedListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        raise NotImplementedError

    def __init__(self, *args, order_by=None, child=None, **kwargs):
        self.order_by = order_by
        assert issubclass(child, serializers.Field)
        kwargs['child'] = child(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def to_representation(self, data):
        if self.order_by:
            assert isinstance(data, models.Manager)
            data = data.order_by(self.order_by)
        return super().to_representation(data)


class OrderedManyRelatedField(serializers.ManyRelatedField):
    def __init__(self, *args, child_relation=None, order_by=None, **kwargs):
        self.order_by = order_by
        assert issubclass(child_relation, serializers.RelatedField)
        list_kwargs = {'child_relation': child_relation(*args, **kwargs)}
        for key in kwargs:
            if key in relations.MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        super().__init__(**list_kwargs)

    def to_representation(self, iterable):
        if self.order_by:
            assert isinstance(iterable, models.QuerySet), \
                "iterable must be queryset"
            iterable = iterable.order_by(self.order_by)
        return super().to_representation(iterable)


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'pk', 'url']


class AssignmentSerializer(serializers.ModelSerializer):
    words = OrderedListSerializer(
        child=SimpleWordSerializer, order_by='wordinassignment', read_only=True)
    characters = OrderedListSerializer(
        child=SimpleCharacterSerializer, order_by='characterinassignment', read_only=True)
    radicals = OrderedListSerializer(
        child=RadicalSerializer, order_by='radicalinassignment', read_only=True)
    word_ids = OrderedManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField,
        source='words', queryset=Word.objects.all(),
        order_by='wordinassignment',
    )
    character_ids = OrderedManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField,
        source='characters', queryset=Character.objects.all(),
        order_by='characterinassignment',
    )
    radical_ids = OrderedManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField,
        source='radicals', queryset=Radical.objects.all(),
        order_by='radicalinassignment'
    )

    def validate(self, data):
        if ('klass' in data
                and data['klass'].teacher.user != self.context['request'].user):
            raise serializers.ValidationError("You don't own this class")
        return data

    def update(self, instance, validated_data):
        """
        a modified version of inherited update method plus a modified version
        of django RelatedManager's set method to enforce the order in through
        models of m2m_fields
        """
        from rest_framework.utils import model_meta
        from rest_framework.serializers import raise_errors_on_nested_writes
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            with transaction.atomic():
                field = getattr(instance, attr)
                old_ids = set(field.values_list('pk', flat=True))
                new_objs = []
                for obj in value:
                    if obj.pk in old_ids:
                        old_ids.remove(obj.pk)
                    else:
                        new_objs.append(obj)
                field.add(*new_objs)
                field.remove(*old_ids)
                through_objs = list(field.through.objects.filter(
                    **{field.source_field_name: instance}))
                for order, obj in enumerate(through_objs):
                    obj.order = value.index(getattr(obj, field.target_field_name))
                field.through.objects.bulk_update(through_objs, ('order',))

        instance.refresh_from_db()
        return instance

    class Meta:
        model = Assignment
        fields = ['name', 'published_time',
                  'words', 'characters', 'radicals',
                  'word_ids', 'character_ids', 'radical_ids']


class ClassSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['url', 'pk', 'name']


class ClassSerializer(serializers.ModelSerializer):
    assignments = AssignmentListSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['pk', 'name', 'assignments']


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    classes = ClassSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['school', 'classes']


class StudentSerializer(serializers.ModelSerializer):
    klass = ClassSimpleSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['klass']


