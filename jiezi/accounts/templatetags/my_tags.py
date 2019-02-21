from django import template

register = template.Library()

@register.simple_tag
def get_user_learned_character_cnt(user):
    return user.user_characters.filter(times_learned__gt=0).count()