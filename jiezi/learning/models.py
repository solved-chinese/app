from django.db import models
import accounts.models  # to avoid cyclic import


def character_path(instance, filename):
    return f'characters/C{instance.__str__()}/{filename}'


def radical_path(instance, filename):
    return f'radicals/R{instance.__str__()}/{filename}'


class Radical(models.Model):
    jiezi_id = models.IntegerField(primary_key=True)
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=10)
    definition = models.CharField(max_length=50)
    mnemonic_image = models.ImageField(upload_to=radical_path, default='default.jpg')  # TODO add height/width
    is_phonetic = models.BooleanField();
    is_semantic = models.BooleanField();

    class Meta:
        ordering = ['jiezi_id']

    def __str__(self):
        return 'R' + '%04d'%self.jiezi_id + ':' + self.chinese


class Character(models.Model):
    jiezi_id = models.IntegerField(primary_key=True)
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=10)
    definition_1 = models.CharField(max_length=50)
    definition_2 = models.CharField(max_length=50, null=True, blank=True)
    explanation_2 = models.CharField(max_length=200, null=True, blank=True)
    definition_3 = models.CharField(max_length=50, null=True, blank=True)
    explanation_3 = models.CharField(max_length=200, null=True, blank=True)

    audio = models.FileField(upload_to=character_path, default='error.mp3')
    color_coded_image = models.ImageField(upload_to=character_path, default='default.jpg')  # TODO add height/width
    stroke_order_image = models.ImageField(upload_to=character_path, default='default.jpg')

    mnemonic_explanation = models.CharField(max_length=200)
    mnemonic_1 = models.IntegerField(help_text="enter number only")
    mnemonic_2 = models.IntegerField(null=True, blank=True,
                                     help_text="enter number only, if it doens't exits, leave BLANK instead of putting 0")
    mnemonic_3 = models.IntegerField(null=True, blank=True,
                                     help_text="enter number only, if it doens't exits, leave BLANK instead of putting 0")

    example_1_word = models.CharField(max_length=5)
    example_1_pinin = models.CharField(max_length=25)
    example_1_character = models.CharField(max_length=50)
    example_1_meaning = models.CharField(max_length=50)
    example_2_word = models.CharField(max_length=5, null=True, blank=True)
    example_2_pinin = models.CharField(max_length=25, null=True, blank=True)
    example_2_character = models.CharField(max_length=50, null=True, blank=True)
    example_2_meaning = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return 'C' + '%04d'%self.jiezi_id + ':' + self.chinese

    # a wrapper of __str__ as template doesn't allow for things starting with _ ...
    def to_string(self):
        return self.__str__()

    class Meta:
        ordering = ['jiezi_id']


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
