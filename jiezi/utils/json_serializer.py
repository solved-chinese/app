from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db.models import Model


def chenyx_serialize(obj):
    """
    This function serialize model objects into python dictionary, use this
    function before you pass the model objects into JsonResponse

    :param obj: the object to be serialized, it could be a model object, list
        of model objects, or queryset
    :return: a python dictionary of serialized object
    """
    if isinstance(obj, Model):
        return serialize('python', [obj])[0]
    elif isinstance(obj, (QuerySet, list)):
        return serialize('python', obj)
    return obj