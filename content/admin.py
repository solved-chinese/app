from django.contrib import admin
from .models import Word, Character, Radical, RadicalInCharacter, \
    CharacterInWord, DefinitionInWord, DefinitionInCharacter, Sentence, \
    WordSet, WordInSet


@admin.register(Radical)
class RadicalAdmin(admin.ModelAdmin):
    search_fields = ['chinese']
    list_filter = ['is_done']
    list_display = ['__str__', 'is_done', 'get_character_list_display']

    def get_character_list_display(self, radical):
        s = ""
        for c in radical.characters.all().distinct():
            s += f"{str(c)}, "
        return s[:-2]
    get_character_list_display.short_description = "Used In"


""" Character Starts """


class RadicalInCharacterInline(admin.TabularInline):
    model = RadicalInCharacter
    autocomplete_fields = ['radical']
    extra = 0


class DefinitionInCharacterInline(admin.TabularInline):
    model = DefinitionInCharacter
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    readonly_fields = ['archive']
    search_fields = ['chinese', 'pinyin']
    list_display = ['__str__', 'is_done', 'get_word_list_display']
    list_filter = ['is_done']
    autocomplete_fields = ["radicals"]
    inlines = [RadicalInCharacterInline, DefinitionInCharacterInline]

    def get_word_list_display(self, character):
        s = ""
        for w in character.words.all().distinct():
            s += f"{str(w)}, "
        return s[:-2]
    get_word_list_display.short_description = "Used In"


""" Word starts """


class CharacterInWordInline(admin.TabularInline):
    model = CharacterInWord
    autocomplete_fields = ['character']
    extra = 0


class DefinitionInWordInline(admin.TabularInline):
    model = DefinitionInWord
    extra = 0


class SentenceInline(admin.TabularInline):
    model = Sentence
    extra = 0


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    search_fields = ['chinese', 'pinyin']
    list_display = ['__str__', 'is_done', 'get_set_list_display']
    list_filter = ['is_done']
    inlines = [CharacterInWordInline, DefinitionInWordInline,
               SentenceInline]

    def get_set_list_display(self, word):
        s = ""
        for set_ in word.word_sets.all():
            s += f"{set_.name}, "
        return s[:-2]
    get_set_list_display.short_description = "Used In"


""" WordSet starts """


class WordInSetInline(admin.TabularInline):
    model = WordInSet
    autocomplete_fields = ['word']


@admin.register(WordSet)
class WordSetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_done']
    list_filter = ['is_done']
    search_fields = ['name', 'characters__chinese']
    inlines = [WordInSetInline]
