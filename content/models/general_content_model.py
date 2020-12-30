from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_chinese_character_or_x(s):
    return RegexValidator('^(([\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]+)|(x))\Z',
                          'this need to be either in Chinese or "x"')


class GeneralContentModel(models.Model):
    note = models.TextField(help_text="This is for internal use only, feel free "
                                      "to use it for note taking",
                            max_length=500, blank=True)
    is_done = models.BooleanField(default=False)

    def get_child_models(self):
        """ This returns all child models in list[name, model] where name is
        a field name of self. Used for validating is_done in clean_field() """
        return []

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        # TODO fine tune this
        assert not exclude or 'is_done' not in exclude or not self.is_done, \
            "Impossible for is_done to be excluded when it is true"

        def handle_error(errors, name, exclude):
            if exclude and field.name in exclude:
                errors['is_done'] = errors.get('is_done', '') + \
                                    f"field {name} not done; "
            else:
                errors[name] = "This field not done"

        if self.is_done:
            if self.pk is None:
                raise ValidationError({'is_done': 'Cannot create a done model '
                                                  'in one step!'})
            errors = {}
            for field in self.__class__._meta.get_fields():
                if isinstance(field, (models.CharField, models.TextField)) and \
                        getattr(self, field.name) == 'TODO':
                    handle_error(errors, field.name, exclude)
                elif isinstance(field, (models.ImageField)) and \
                        getattr(self, field.name) == 'default.jpg':
                    handle_error(errors, field.name, exclude)
            for name, obj in self.get_child_models():
                assert isinstance(obj, GeneralContentModel)
                if not obj.is_done:
                    errors['is_done'] = errors.get('is_done', '') + \
                                        f"{name} not done; "
            if errors:
                errors['is_done'] = errors.get('is_done', '') + \
                                    "something is not done"
                raise ValidationError(errors)

    def reset_order(self):
        pass

    class Meta:
        abstract = True


class OrderableMixin(models.Model):
    order = models.FloatField(default=0,
        help_text="This determines the order of the elements")

    @classmethod
    def reset_order(cls, manager):
        objects = list(manager.all())
        for index, obj in enumerate(objects):
            obj.order = index
            obj.save()

    class Meta:
        abstract = True
