from drf_spectacular.openapi import AutoSchema, get_doc
from rest_framework.schemas.inspectors import ViewInspector


class MyAutoSchema(AutoSchema):
    def get_description(self):
        return ViewInspector.get_description(self, self.path, self.method)

    def get_summary(self):
        """
        reference https://github.com/axnsan12/drf-yasg/blob/d2778708f6a1d50dee2bdcaee428cf8014afc3ec/src/drf_yasg/inspectors/view.py
        modified that one line description becomes summary
        """
        summary = None
        summary_max_len = 120
        description = self.get_description()
        sections = description.split('\n\n', 1)
        if len(sections) == 2:
            sections[0] = sections[0].strip()
            if len(sections[0]) < summary_max_len:
                summary, description = sections
        elif '\n' not in description and len(description) < summary_max_len:
            summary = description
        return summary
