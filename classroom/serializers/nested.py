from django.db import transaction
from rest_framework import serializers

from classroom.models import Class, Assignment, Student, Teacher
from classroom.serializers import AssignmentSimpleSerializer, StudentSimpleSerializer, ClassSimpleSerializer
from content.models import Word, Character, Radical
from content.serializers import SimpleWordSerializer, SimpleCharacterSerializer, RadicalSerializer
from jiezi.rest.serializers import OrderedListSerializer, OrderedManyRelatedField


__all__ = ['ClassSerializer', 'AssignmentSerializer', 'StudentSerializer',
           'TeacherSerializer']


class ClassSerializer(ClassSimpleSerializer):
    assignments = AssignmentSimpleSerializer(many=True, read_only=True)
    students = StudentSimpleSerializer(many=True, read_only=True)
    student_ids = serializers.PrimaryKeyRelatedField(
        many=True, source='students', queryset=Student.objects.all())

    def validate_student_ids(self, value):
        new_students = set(value)
        if self.instance is None:
            old_students = set()
        else:
            old_students = set(self.instance.students.all())
        if not new_students.issubset(old_students):
            raise serializers.ValidationError(
                "new students are not subset of old students."
                "`student_ids` is used to remove students from a class, "
                "it is not allowed to add students from the teacher's side.")
        return value

    class Meta:
        model = Class
        fields = ['pk', 'teacher', 'students', 'student_ids', 'name',
                  'assignments', 'code']
        read_only_fields = ['code']


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
        fields = ['name', 'klass', 'published_time',
                  'words', 'characters', 'radicals',
                  'word_ids', 'character_ids', 'radical_ids']


class StudentSerializer(serializers.ModelSerializer):
    class_code = serializers.SlugRelatedField(
        source='klass', slug_field='code',
        queryset=Class.objects.all(), allow_null=True,
    )
    klass = ClassSimpleSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['klass', 'class_code']


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    classes = ClassSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['school', 'classes']