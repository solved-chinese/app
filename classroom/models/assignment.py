import pandas as pd
from django.db import models
from django_pandas.io import read_frame

from learning.models import ReviewManager


class Assignment(models.Model):
    # TODO test assignment
    in_class = models.ForeignKey('Class', on_delete=models.CASCADE,
                                 related_name='assignments',
                                 related_query_name='assignment')
    character_set = models.ForeignKey('content.CharacterSet',
                                      on_delete=models.CASCADE,
                                      related_name='assignments',
                                      related_query_name='assignment')
    review_manager = models.ForeignKey('learning.ReviewManager',
                                       on_delete=models.PROTECT,
                                       related_name='+',
                                       default=ReviewManager.get_default_pk)
    published_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_modified_time']
        unique_together = ['in_class', 'character_set']

    def save(self, *args, **kwargs):
        is_adding = self._state.adding
        super().save(*args, **kwargs)
        if is_adding:
            self.in_class.notify_students(
                f'An new assignment "{self.name}" has been published.')

    def get_stats(self):
        from learning.models import SCAbility, StudentCharacter
        students = self.in_class.students.all()
        if not students.exists():
            return {"stats_error": "There are no students in this class"}
        abilities = self.review_manager.monitored_abilities.all()
        characters = self.character_set.characters.all()
        if not characters.exists():
            return {"stats_error": "There are no characters in this assignment"}
        characters_cnt = characters.count()
        sca_qs = SCAbility.objects.filter(
            student__in=students,
            character__in=characters,
            ability__in=abilities,
            state__gt=SCAbility.TO_LEARN,
        )
        sca_frame = read_frame(sca_qs,
            fieldnames=['state', 'character__id', 'accuracy',
                        'ability', 'student__user__id']
        ).rename(columns={'student__user__id': 'user__id'})
        sc_qs = StudentCharacter.objects.filter(
            student__in=students, character__in=characters
        )
        sc_frame = read_frame(
            sc_qs,
            fieldnames=['character__id', 'accuracy']
        )

        a_cnt_frame = sca_frame.groupby(['user__id', 'character__id', 'state'],
                                        as_index=False)['ability'].count()
        mastered = (a_cnt_frame['state'] == 'Mastered') \
                   & (a_cnt_frame['ability'] == abilities.count())

        # Student frame
        s_mastered_series = a_cnt_frame[mastered].groupby('user__id').size()
        s_mastered_series.name = 'Mastered'
        s_in_progress_series = a_cnt_frame[~mastered].groupby('user__id').size()
        s_in_progress_series.name = 'In Progress'
        s_frame = read_frame(students,
                             fieldnames=['user__display_name'],
                             index_col='user__id')
        s_frame['To Learn'] = characters_cnt
        s_frame = pd.concat([s_frame, s_in_progress_series, s_mastered_series],
                          axis=1).fillna(0)
        s_frame['To Learn'] -= s_frame['In Progress'] + s_frame['Mastered']
        s_frame = s_frame.set_index('user__display_name').rename_axis('student')
        finished = (s_frame['Mastered'] == characters_cnt)
        finished_cnt = finished.sum()
        total_student_cnt = students.count()
        s_frame.insert(0, 'Completion Status', finished)
        s_frame.loc['Average'] = s_frame.mean()
        s_frame = s_frame.astype(int)
        s_frame['Completion Status'] = s_frame['Completion Status'].apply(
            lambda x: '√' if x else "")
        s_frame = s_frame.style.set_table_attributes('class="table"').\
            render()

        if not sc_qs.exists() or not sca_qs.exists():
            c_frame = "<p>The stats will be calculated when your " \
                      "students start learning</p>"
        else:
            c_frame = read_frame(characters, fieldnames=['chinese'], index_col='id')
            c_mastered_series = (a_cnt_frame[mastered].groupby('character__id')
                .size() / total_student_cnt).rename("Mastered Percentage")
            c_accuracy_series = sc_frame.dropna().groupby('character__id')\
                ['accuracy'].mean().rename("Average Overall Accuracy")
            a_accuracy_frame = sca_frame.dropna().groupby(
                ['character__id', 'ability'])['accuracy'].mean().unstack()\
                .rename(lambda x:f"accuracy of {x}", axis='columns')
            c_frame = pd.concat([c_frame, c_mastered_series, c_accuracy_series,
                                 a_accuracy_frame], axis=1)
            c_frame = c_frame.set_index('chinese').rename_axis('character')
            c_frame = c_frame.style.set_table_attributes('class="table"').\
                format(lambda x: f"{x:.0%}", na_rep='--').\
                set_caption('"--" means that no student has learned this yet.').\
                render()

        return {
            "finished_student_cnt": finished_cnt,
            "total_student_cnt": total_student_cnt,
            "student_frame": s_frame,
            "character_frame": c_frame,
        }

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('assignment_detail', args=[self.pk])

    @staticmethod
    def remove_testers(queryset):
        from accounts.models import User
        filter_kwargs = {f"in_class__teacher__user__{key}": value
            for key, value in User.REMOVE_TESTER_FILTER_KWARGS.items()}
        exclude_kwargs = {f"in_class__teacher__user__{key}": value
            for key, value in User.REMOVE_TESTER_EXCLUDE_KWARGS.items()}
        return queryset.filter(**filter_kwargs).exclude(**exclude_kwargs)

    @property
    def name(self):
        return self.character_set.name

    def __str__(self):
        return f'Assignment: {self.name}'

    def __repr__(self):
        return f'<Assignment {self.name} in {repr(self.in_class)}>'
