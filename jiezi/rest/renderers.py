import json

from rest_framework.renderers import BrowsableAPIRenderer
from django import forms


def _get_raw_form(content):
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


class CustomActionsBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    This class enables overriding the POST & PUT form in REST BrowsableAPI
    through the two optional attributes `POST_action` and `PUT_action` of any
    class-based views. Each action tag should be a dictionary with the keys
    being the required arguments and values being dictionaries describing the
    keys. The `example` key of the value dictionary will be set as the form
    default.
    Also it is possible to override the context of the BrowsableAPI page
    directly through the optional `api_context` attribute.
    reference search in
    https://github.com/solved-chinese/app/blob/v0.1/content/views.py
    """
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
                context[f'raw_data_{method.lower()}_form'] = _get_raw_form(
                    json.dumps(content))
                # if a raw_POST form is overriden, it means that the HTML POST
                # form is out of date and should not be displayed
                context[f'{method.lower()}_form'] = None
                context['display_edit_forms'] = True
            except AttributeError:
                pass

        if hasattr(view, 'api_context'):
            context.update(view.api_content)
        return context
