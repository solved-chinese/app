from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db.models import Model
from collections.abc import Iterable


def deep_serialize(list_to_serialize, fields_to_expand=None):
    """
    This function extends the default serialize function to enable
    serialization of foreign keys
    :param list_to_serialize: a iterable to be serialize
    :param fields_to_expand: list of the name of the fields of foreign keys to
    be serialized
    :return: the same as serialize but with fields_to_expand being a list of
    serialized objects instead of a list of pk's
    """
    rv = []
    for obj in list_to_serialize:
        serialized_obj = serialize('python', [obj])[0]
        for field in fields_to_expand:
            field_content = []
            for field_obj in getattr(obj, field).iterator():
                field_content.append(serialize('python', [field_obj])[0])
            serialized_obj['fields'][field] = field_content
        rv.append(serialized_obj)
    return rv


def chenyx_serialize(obj, fields_to_expand=None):
    """
    This function extends the deep_serialize function to enable serialization
    of model object as well as queryset
    """
    if isinstance(obj, Model):
        return deep_serialize([obj], fields_to_expand)[0]
    elif isinstance(obj, QuerySet):
        return deep_serialize(obj.iterator(), fields_to_expand)
    elif isinstance(obj, Iterable):
        return deep_serialize(obj, fields_to_expand)

    raise TypeError(f'obj has to be of type Model, QuerySet, or Iterable but \
        is {type(obj)}')