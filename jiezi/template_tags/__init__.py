from django import template
from .pretty_duration import pretty_duration


ALL_TAGS = [pretty_duration]

register = template.Library()

for tag in ALL_TAGS:
    register.filter(tag.__name__, tag)
