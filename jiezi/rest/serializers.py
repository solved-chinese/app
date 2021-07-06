from django.db import models
from rest_framework import serializers, relations


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