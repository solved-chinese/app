from collections import OrderedDict

from rest_framework.metadata import SimpleMetadata


class CustomActionsMetadata(SimpleMetadata):
    """
    This class enables overriding the actions key for OPTION requests.
    To override, set attributes `POST_action` or `GET_action` in a view class.

    At the same time, it modifies the OPTION response to return permissions
    """
    def determine_metadata(self, request, view):
        metadata = OrderedDict()
        metadata['name'] = view.get_view_name()
        metadata['description'] = view.get_view_description()
        metadata['permissions'] = [str(cls) for cls in view.permission_classes]
        actions = {}
        if hasattr(view, 'get_serializer'):
            actions = self.determine_actions(request, view)
        actions = self.get_custom_actions(request, view, actions)
        if actions:
            metadata['actions'] = actions
        return metadata

    def get_custom_actions(self, request, view, actions):
        for method in set(view.allowed_methods):
            try:
                action = getattr(view, f'{method}_action')
                if not action:
                    del actions[method]
                else:
                    actions[method] = action
            except (AttributeError, KeyError):
                pass
        return actions
