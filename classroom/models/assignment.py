import pandas as pd

from django.db import models
from django_pandas.io import read_frame

from learning.models import LearningProcess, Record


class Assignment(models.Model):
    klass = models.ForeignKey('Class', on_delete=models.CASCADE,
                              related_name='assignments',
                              related_query_name='assignment')
    wordset = models.ForeignKey('content.WordSet',
                                on_delete=models.CASCADE,
                                related_name='assignments',
                                related_query_name='assignment')
    published_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_modified_time']
        unique_together = ['klass', 'wordset']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('assignment_detail', args=[self.pk])

    def get_stats(self):
        processes = LearningProcess.objects.filter(
            user__student__in=self.klass.students.all(),
            wordset=self.wordset,
        )
        # student dataframe
        sdf = read_frame(
            processes,
            fieldnames=[
                'data__progress_bar__mastered',
                'data__progress_bar__familiar',
                'data__progress_bar__remaining',
                'data__stats__correct_answer',
                'data__stats__wrong_answer'],
            verbose=False,
            index_col='user__id',
        )
        sdf.columns = ['mastered', 'familiar', 'remaining', 'correct', 'wrong']
        sdf.insert(1, 'Accuracy', sdf['correct'] / sdf['correct'] + sdf['wrong'])
        sdf.insert(1, 'Completion', sdf['mastered'] /
                   (sdf['mastered'] + sdf['familiar'] + sdf['remaining']))
        sdf = sdf.drop(columns=['mastered', 'familiar', 'remaining',
                                'correct', 'wrong'])
        # add students who have not started yet
        students = read_frame(self.klass.students.all(),
                              fieldnames=['user__display_name'],
                              index_col='user__id')
        students.columns = ['Student']
        sdf = pd.concat([students, sdf], axis=1, sort=True)
        # completion check
        sdf = sdf.fillna(0)
        sdf = sdf.sort_values('Completion', ascending=False)
        percent_format = lambda x: f"{int(x * 20) * 5}%"
        sdf = sdf.style\
            .format({'Completion': percent_format, 'Accuracy': percent_format})\
            .set_table_attributes('class="table"').hide_index().render()

        # word dataframe
        records = Record.objects.filter(
            user__student__in=self.klass.students.all(),
            learning_process__wordset=self.wordset,
            reviewable__word__isnull=False,
            action__in=(Record.Action.CORRECT_ANSWER, Record.Action.WRONG_ANSWER)
        )
        wdf = read_frame(records,
                         fieldnames=['reviewable__word__chinese', 'action'],
                         verbose=False)
        wdf.columns = ['word', 'action']
        correct_index = wdf['action'] == Record.Action.CORRECT_ANSWER
        correct_cnt = wdf[correct_index].groupby('word').size()
        wrong_cnt = wdf[~correct_index].groupby('word').size()
        wdf = pd.concat([correct_cnt, wrong_cnt], axis=1, sort=True).fillna(0)
        wdf.columns = ['correct_cnt', 'wrong_cnt']
        wdf['total_cnt'] = wdf['correct_cnt'] + wdf['wrong_cnt']
        wdf = wdf[wdf['total_cnt'] >= 3]
        wdf['Accuracy'] = wdf['correct_cnt'] / wdf['total_cnt']
        wdf = wdf.drop(columns=['correct_cnt', 'wrong_cnt', 'total_cnt'])
        wdf = wdf.sort_values('Accuracy', ascending=True)
        wdf = wdf.style.format(percent_format)\
            .set_table_attributes('class="table"')\
            .set_caption('Only showing words that have been learned '
                         'at least 3 times')\
            .render()
        return {'student_stats': sdf, 'word_stats': wdf}

    @property
    def name(self):
        return self.wordset.name

    def __str__(self):
        return f'Assignment: {self.name}'

    def __repr__(self):
        return f'<Assignment {self.name} in {repr(self.klass)}>'
