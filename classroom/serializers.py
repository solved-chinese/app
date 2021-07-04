from django.db import transaction, models
from rest_framework import serializers

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

    class Meta:
        model = Assignment
        fields = ['name', 'published_time', 'words',
                  'characters', 'radicals']


class AssignmentUpdateSerializer(serializers.ModelSerializer):
    words = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Word.objects.all())
    characters = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Character.objects.all())
    radicals = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Radical.objects.all())

    def validate(self, data):
        if data['klass'].teacher.user != self.context['request'].user:
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
        fields = ['klass', 'name', 'words', 'characters', 'radicals']


class ClassSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['url', 'pk', 'name']


class ClassSerializer(serializers.ModelSerializer):
    assignments = AssignmentListSerializer(many=True, read_only=True)

    # def create(self, validated_data):
    #     validated_data['teacher'] = self.context['request'].user.teacher
    #     return super().create(validated_data)

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


