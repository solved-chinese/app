from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from content.models import Radical


@admin.register(Radical)
class RadicalAdmin(admin.ModelAdmin):
    search_fields = ['chinese']
    list_filter = ['is_done']
    list_display = ['__str__', 'is_done', 'get_image_thumbnail',
                    'get_character_list_display']
    readonly_fields = ['get_image_preview']

    def get_character_list_display(self, radical):
        s = ""
        for c in radical.characters.all().distinct():
            s += f"<a href={reverse('admin:content_character_change', args=[c.pk])}>" \
                 f"{c.chinese}</a>, "
        return format_html(s[:-2])
    get_character_list_display.short_description = "Used In"

    def get_image_thumbnail(self, radical):
        return format_html('<img src="%s" width="30" height="30" />' % (radical.image.url))
    get_image_thumbnail.short_description = "image thumbnail"

    def get_image_preview(self, radical):
        return format_html('<img src="%s" width="150" height="150" />' % (radical.image.url))

    get_image_preview.short_description = "image preview"