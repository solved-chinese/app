from django.db import models
import accounts.models  # to avoid cyclic import


class Radical(models.Model):
    id = models.IntegerField(primary_key=True)
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=10)
    definition = models.CharField(max_length=50)
    mnemonic_explanation = models.TextField(max_length=100, null=True, blank=True)
    mnemonic_image = models.ImageField(default='default.jpg')
    is_phonetic = models.BooleanField()
    is_semantic = models.BooleanField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return 'R' + '%04d' % self.jiezi_id + ':' + self.chinese


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=6)
    part_of_speech_1 = models.CharField(max_length=50)
    definition_1 = models.CharField(max_length=50)
    part_of_speech_2 = models.CharField(max_length=50)
    definition_2 = models.CharField(max_length=50, null=True, blank=True)
    explanation_2 = models.CharField(max_length=200, null=True, blank=True)
    part_of_speech_3 = models.CharField(max_length=50)
    definition_3 = models.CharField(max_length=50, null=True, blank=True)
    explanation_3 = models.CharField(max_length=200, null=True, blank=True)

    radical_1_id = models.IntegerField()
    radical_2_id = models.IntegerField(null=True, blank=True)
    radical_3_id = models.IntegerField(null=True, blank=True)
    #for accessing characters from radicals
    radicals = models.ManyToManyField(Radical, related_name="characters", related_query_name="character")
    mnemonic_explanation = models.TextField(max_length=200)

    example_1_word = models.CharField(max_length=5)
    example_1_pinyin = models.CharField(max_length=25)
    example_1_character = models.CharField(max_length=50)
    example_1_meaning = models.CharField(max_length=50)
    example_2_word = models.CharField(max_length=5, null=True, blank=True)
    example_2_pinyin = models.CharField(max_length=25, null=True, blank=True)
    example_2_character = models.CharField(max_length=50, null=True, blank=True)
    example_2_meaning = models.CharField(max_length=50, null=True, blank=True)

    is_preview_definition = models.BooleanField()
    is_preview_pinyin = models.BooleanField()

    color_coded_image = models.ImageField(default='default.jpg')
    stroke_order_image = models.ImageField(default='default.jpg')
    small_color_coded = models.ImageField(default='default.jpg')

    def __str__(self):
        return 'C' + '%04d' % self.jiezi_id + ':' + self.chinese

    class Meta:
        ordering = ['id']


class CharacterSet(models.Model):
    characters = models.ManyToManyField(Character)
    name = models.CharField(max_length=50)

    def add_to_user(self, user):
        if user.user_character_tags.filter(name=self.name).exists():
            raise Exception('ERROR: a set with the same name already exists')
        tag = accounts.models.UserCharacterTag.objects.create(name=self.name, user=user)
        for character in self.characters.all():
            character_to_add = accounts.models.UserCharacter.objects.get_or_create(
                character=character, user=user)[0]
            tag.user_characters.add(character_to_add)

    def __str__(self):
        return self.name
