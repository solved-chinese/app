import html

from django.db import models


class DFModelMixin:
    """
    This mixin provides a update_from_df method for all models that rely on
    dataframe to update its objects.
    The id field as primary key is mandatory

    Fields are pulled from dataframe as such:
    if field blank, set value to None
    if Integer/Boolean/String, direct conversion
    if ForeignField/OneToOneFIeld, find using pk
    if ManyToManyField, add the pks of all columns with the same field name

    :param df: A Dataframe object
    :return: a dict (id: msg) where msg is a HTML div ready for display
    """
    id = models.IntegerField(primary_key=True)

    @classmethod
    def update_from_df(cls, df):
        """
        This function pulls the models from the given dataframe.
        Every row of the Dataframe object must represent a object, with a
        mandatory field id.

        """
        df.replace('', None, inplace=True)
        df.fillna(0, inplace=True)
        messages = []
        good_pk = []
        m2m_fields = []
        for field in cls._meta.get_fields():
            if isinstance(field, models.ManyToManyField):
                m2m_fields.append(field)
        for i, row in df.iterrows():
            try:
                id = row['id']
                if id == 0:
                    messages.append(f'ERR at start : row {i} id not found')
                    continue
                # TODO make this a special validator
                if '√' not in str(row['Comments']):
                    if cls.objects.filter(pk=id).exists():
                        messages.append(f'WARNING: delete id={id} due to no '
                                        f'check in comment')
                    else:
                        messages.append(f'IGNORE: ignore id={id} due to no '
                                        f'check in comment')
                    continue
                data = {}
                for field in cls._meta.get_fields():
                    if field.name == 'id':
                        continue
                    if isinstance(field,
                                  (models.IntegerField, models.BooleanField)):
                        data[field.name] = row[field.name]
                    elif isinstance(field, models.CharField):
                        # FIXME per request of LING team, remove all stars from str
                        data[field.name] = row[field.name].strip().replace('*', '') \
                            if row[field.name] else None
                    elif isinstance(field, (models.OneToOneField,
                                            models.ForeignKey)):
                        data[field.name] = \
                            field.related_model.objects.get(pk=row[field.name]) \
                                if row[field.name] else None

            except Exception as e:
                try:
                    field
                except NameError:
                    field = None
                messages.append(
                    f'ERR getting field {field} of id={id}: {repr(e)}')
                continue

            try:
                obj, is_created = cls.objects.update_or_create(id=id,
                                                               defaults=data)
                row = row.groupby(level=0).agg(list).to_dict()
                warning = ""
                for field in m2m_fields:
                    pks = row[field.name]
                    related_objs = []
                    for pk in pks:
                        pk = int(pk)
                        if not pk:
                            continue
                        try:
                            related_obj = field.related_model.objects.get(pk=pk)
                            related_objs.append(related_obj)
                        except field.related_model.DoesNotExist:
                            warning += f'\n{field} has no related object ' \
                                       f'with id={pk}'
                    getattr(obj, field.name).set(related_objs)
                if warning:
                    warning = f'WARNING though completed: {warning}\n'
                messages.append(f"{warning}"
                                f"{'create' if is_created else 'update'} "
                                f"{repr(obj)}")
                good_pk.append(id)
            except Exception as e:
                messages.append(f'ERR constructing id={id}: {repr(e)}')

        for i, msg in enumerate(messages, 0):
            msg = f'<pre>{html.escape(msg)}</pre>'
            if msg[5] == 'E':
                messages[i] = '<div style="color:red;">' + msg + '</div>'
            elif msg[5] == 'W':
                messages[i] = '<div style="color:orange;">' + msg + '</div>'
            elif msg[5] == "I":
                messages[i] = '<div style="color:gray;">' + msg + '</div>'
            else:
                messages[i] = '<div style="color:green;">' + msg + '</div>'

        bad_queryset = cls.objects.exclude(pk__in=good_pk)
        if bad_queryset.exists():
            bad_msg = f"The following objects are not updated correctly: " \
                      f"{[repr(obj) for obj in bad_queryset.all()]}. " \
                      f"If you wish to delete them, " \
                      f"save this page's html and contact chenyx." \
                      f"{[obj.pk for obj in bad_queryset.all()]}"
            messages.insert(0, '<div style="color:red;">' +
                            html.escape(bad_msg) + '</div>')

        return messages
