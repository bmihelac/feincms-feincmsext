from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured


def load_class(class_path):
    """
    Loads a class given a class_path.
    """
    class_module, class_name = class_path.rsplit('.', 1)
    mod = import_module(class_module)
    clazz = getattr(mod, class_name)
    return clazz


def create_content_types(cls, content_types_conf):
    """
    Create content types for given ``content_types_conf``.

    ``content_types_conf`` is a list or tuple, each element should have
    content type configuration. 

    Content type configuration is list or tuple with following elements:

    * content_type - class path or model (can be list)
    * region - region (optional, can be list)
    * options - dictionary to pass as options (optional)

    >>> content_types = [
            (RichTextContent, ), # all regions
            (
                ('feincms.content.video.models', MediaFileContent), # multiple content types
                ('main', 'sidebar'), # multiple regions
                {'TYPE_CHOICES': (('block', 'block'),), # options
            )
            ]
    >>> create_content_type(Page, content_types)
    """
    for conf in content_types_conf:
        content_types, regions, kwargs = (conf + (None, None))[:3]
        if not kwargs:
            kwargs = {}
        if not isinstance(content_types, (list, tuple,)):
            content_types = (content_types,)
        if regions:
            kwargs['regions'] = regions
        for content_type in content_types:
            if isinstance(content_type, basestring):
                try:
                    content_type = load_class(content_type)
                except Exception:
                    raise ImproperlyConfigured("Error importing %s" % content_type)
            cls.create_content_type(content_type, **kwargs)
