from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


class GeneralContentModel(models.Model):
    note = models.TextField(help_text="This is for internal use only, feel free "
                                      "to use it for note taking",
                            max_length=500, blank=True)
    archive = models.TextField(help_text="This is auto-generated as reference. "
                                         "Read-only",
                               max_length=500, blank=True)
    is_done = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.pk is None and self.is_done:
            raise ValidationError('Cannot create a done model in one step!')

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        def handle_error(errors, name, exclude):
            if exclude and field.name in exclude:
                errors[NON_FIELD_ERRORS] = errors.get(NON_FIELD_ERRORS, '') + \
                                    f"field {name} not done; "
            else:
                errors[name] = "This field not done"

        if self.is_done:
            if self.pk is None:
                raise ValidationError('Cannot create a done model in one step!')
            errors = {}
            for field in self.__class__._meta.get_fields():
                if isinstance(field, (models.CharField, models.TextField)) and \
                        'TODO' in getattr(self, field.name):
                    handle_error(errors, field.name, exclude)
                elif isinstance(field, (models.ImageField)) and \
                        getattr(self, field.name) == 'default.jpg':
                    handle_error(errors, field.name, exclude)
            if errors:
                raise ValidationError(errors)

    def reset_order(self):
        pass

    def save(self, *args, check_chinese=True, **kwargs):
        """ gives warning if there are other objects with the same chiense """
        if self._state.adding:
            if check_chinese and hasattr(self, 'chinese') \
                    and self.chinese != 'x':
                others = self.__class__.objects.filter(chinese=self.chinese).\
                    exclude(pk=self.pk)
                if others.exists():
                    others = list(others)
                    self.add_warning(f"there are other objects with "
                                     f"same chinese {others}")
        super().save(*args, **kwargs)

    def add_warning(self, warning):
        self.note += f"\r\n[WARNING] {warning} [END WARNING]"

    class Meta:
        abstract = True
        ordering = ['id']


class OrderableMixin(models.Model):
    order = models.FloatField(default=99,
        help_text="This determines the order of the elements")

    @classmethod
    def reset_order(cls, manager):
        objects = list(manager.all())
        for index, obj in enumerate(objects):
            obj.order = index
            obj.save()

    class Meta:
        abstract = True
