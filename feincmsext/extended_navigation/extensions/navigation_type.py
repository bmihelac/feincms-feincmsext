from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from feincms import extensions


DEFAULT_NAVIGATION_TYPE_CHOICES = (
    ('primary_links', _('primary links')),
    ('secondary_links', _('secondary links')),
)
navigation_type_choices = getattr(settings, "NAVIGATION_TYPE_CHOICES", DEFAULT_NAVIGATION_TYPE_CHOICES)

def register(cls, admin_cls):
    cls.add_to_class('navigation_type', models.CharField(_('navigation type'),
        max_length=32, choices=navigation_type_choices, default=navigation_type_choices[0][0]))

    if hasattr(admin_cls, 'add_extension_options'):
        admin_cls.add_extension_options('navigation_type')
    else:
        admin_cls.fieldsets[0][1]['fields'].extend(['navigation_type',])


class NavigationTypeExtension(extensions.Extension):
    """
    ``NAVIGATION_TYPE_CHOICES`` - from settings.py
    """

    def handle_model(self):
        self.model.add_to_class(
            'navigation_type',
            models.CharField(_('navigation type'),
                             max_length=32,
                             choices=navigation_type_choices,
                             default=navigation_type_choices[0][0]))

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options('navigation_type')
