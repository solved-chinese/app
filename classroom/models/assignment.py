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
        from learning.models import SCAbility
        students = self.in_class.students.all()
        abilities = self.review_manager.monitored_abilities.all()
        characters = self.character_set.characters.all()
        characters_cnt = characters.count()
        qs = SCAbility.objects.filter(
            student__in=students,
            character__in=characters,
            ability__in=abilities,
            state__gt=SCAbility.TO_LEARN,
        )
        students_frame = read_frame(students,
                                    fieldnames=['user__display_name'],
                                    index_col='user_id')
        students_frame['To Learn'] = characters_cnt
        sca_frame = read_frame(qs,
                               fieldnames=['state', 'character',
                                           'ability', 'student__user_id'])
        sca_frame.rename(columns={'student__user_id': 'user_id'}, inplace=True)
        sca_frame = sca_frame.groupby(['user_id', 'character', 'state'],
                                      as_index=False).count()
        mastered = (sca_frame['state'] == 'Mastered') \
                   & (sca_frame['ability'] == abilities.count())
        mastered_series = sca_frame[mastered].groupby('user_id')[
            'character'].count()
        mastered_series.name = 'Mastered'
        in_progress_series = sca_frame[~mastered].groupby('user_id')[
            'character'].count()
        in_progress_series.name = 'In Progress'
        s_frame = pd.concat([students_frame, in_progress_series, mastered_series],
                          axis=1).fillna(0)
        s_frame['To Learn'] -= s_frame['In Progress'] + s_frame['Mastered']
        s_frame.set_index('user__display_name', inplace=True)
        finished = (s_frame['Mastered'] == characters_cnt)
        finished_cnt = finished.sum()
        total_student_cnt = students.count()
        s_frame['Finished'] = finished
        s_frame.loc['Average'] = s_frame.mean()
        return {
            "finished_student_cnt": finished_cnt,
            "total_student_cnt": total_student_cnt,
            "student_frame": s_frame.to_html(classes='table', index_names=False),
        }

    @property
    def name(self):
        return self.character_set.name

    def __str__(self):
        return f'Assignment in {self.in_class}'

    def __repr__(self):
        return f'<Assignment in {repr(self.in_class)}>'
