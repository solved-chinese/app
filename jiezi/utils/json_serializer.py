from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db.models import Model


def chenyx_serialize(obj):
    if isinstance(obj, Model):
        return serialize('python', [obj])[0]
    elif isinstance(obj, (QuerySet, list)):
        return serialize('python', obj)
    return obj