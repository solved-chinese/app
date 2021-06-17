from .renderers import CustomActionsBrowsableAPIRenderer
from djangorestframework_camel_case.render import CamelCaseBrowsableAPIRenderer


class CamelCaseCustomActionBrowsableAPIRenderer(
        CustomActionsBrowsableAPIRenderer, CamelCaseBrowsableAPIRenderer):
    pass
