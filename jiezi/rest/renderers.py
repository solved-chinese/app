import json

from rest_framework.renderers import BrowsableAPIRenderer
from django import forms


def get_raw_form(content):
    class GenericContentForm(forms.Form):
        _content_type = forms.ChoiceField(
            label='Media type',
            choices=[('application/json', 'application/json')],
            initial='application/json',
            widget=forms.Select(attrs={'data-override': 'content-type'})
        )
        _content = forms.CharField(
            label='Content',
            widget=forms.Textarea(attrs={'data-override': 'content'}),
            initial=content,
            required=False
        )
    return GenericContentForm()


class MyBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type,
                                      renderer_context)

        view = renderer_context['view']
        for method in {'POST', 'PUT'} & set(view.allowed_methods):
            try:
                action = getattr(view, f'{method}_action')
                if not action: # in case action is to delete default
                    continue
                content = {}
                for key, description in action.items():
                    content[key] = description.get('example', None)
                context[f'raw_data_{method.lower()}_form'] = get_raw_form(
                    json.dumps(content))
                context[f'{method.lower()}_form'] = None
                context['display_edit_forms'] = True
            except AttributeError:
                pass

        if hasattr(view, 'api_context'):
            context.update(view.api_content)
        return context
