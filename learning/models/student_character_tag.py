from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from classroom.models import Student
from content.models import CharacterSet
from learning.models import StudentCharacter


class SCTagQuerySet(models.QuerySet):
    def check_update(self):
        for sc_tag in self.all():
            sc_tag.check_update()


class SCTagManager(models.Manager):
    def get_queryset(self):
        queryset = SCTagQuerySet(model=self.model, using=self._db)
        return queryset

    def filter_by_pk(self, pk):
        if isinstance(pk, int):
            return self.get_queryset().filter(pk=pk)
        return self.get_queryset().filter(pk__in=pk)


class StudentCharacterTag(models.Model):
    """
    This class connects a student with a character set. It syncs the changes
    from CharacterSet.
    """
    character_set = models.ForeignKey(CharacterSet,
                                      on_delete=models.CASCADE,
                                      related_name='sc_tags',
                                      related_query_name='sc_tag')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='sc_tags',
                                related_query_name='sc_tag')
    # lazy tag
    is_updated = models.BooleanField(default=False)
    student_characters = models.ManyToManyField(StudentCharacter,
                                                related_name='sc_tags',
                                                related_query_name='sc_tag')
    objects = SCTagManager()

    def check_update(self):
        """
        This method ensures that the relationship between this StudentCharacterTag
        and its UserCharacters follows that between its CharacterSet and the
        corresponding Characters
        """
        if self.is_updated:
            return
        scs = [StudentCharacter.of(self.student, character)
               for character in self.character_set.characters.all()]
        self.student_characters.set(scs)
        self.is_updated = True
        self.save()

    @property
    def states_count(self):
        d = {}
        for num, choice in StudentCharacter.STATE_CHOICES:
            if choice != 'To Learn':
                d[choice] = StudentCharacter.objects.filter(
                    state=num,
                    character__in=self.character_set.characters.all()
                ).count()
        d['To Learn'] = self.character_set.characters.count() \
                    - sum(d.values())
        return d

    @classmethod
    def of(cls, student, cset):
        return cls.objects.update_or_create(student=student,
                                             character_set=cset)[0]

    @property
    def name(self):
        return self.character_set.name

    def __str__(self):
        return f"<sct {self.pk}:{self.student}'s {self.character_set.name}>"

    def __repr__(self):
        return f"<sct {self.pk}:{self.student}'s {self.character_set}>"

    class Meta:
        unique_together = ('student', 'character_set')


@receiver(m2m_changed, sender=CharacterSet.characters.through)
def update_sc_tag_from_cset(sender, **kwargs):
    action = kwargs['action']
    if action == 'post_add':
        cset = kwargs['instance']
        StudentCharacterTag.objects.filter(character_set=cset)\
            .update(is_updated=False)
