from django.db import models
import accounts.models  # to avoid cyclic import


class Character(models.Model):
    chinese = models.CharField(max_length=30)
    english = models.CharField(max_length=100)

    def __str__(self):
        return self.chinese + ', ' + self.english

    # template doesn't allow for things starting with _
    def to_string(self):
        return self.__str__()

    class Meta:
        unique_together = (('chinese', 'english'),)


class CharacterSet(models.Model):
    characters = models.ManyToManyField(Character)
    name = models.CharField(max_length=50)

    def add_to_user(self, user):
        if user.user_character_tags.filter(name=self.name).exists():
            raise accounts.models.UserCharacterTag.SameNameException
        tag = accounts.models.UserCharacterTag.objects.create(name=self.name, user=user)
        for character in self.characters.all():
            print(character.__str__())
            character_to_add = accounts.models.UserCharacter.objects.get_or_create(character=character, user=user)[0]
            tag.user_characters.add(character_to_add)

    def __str__(self):
        return self.name
