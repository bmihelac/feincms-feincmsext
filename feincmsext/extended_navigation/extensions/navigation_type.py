from django.db import models
from django.utils.translation import ugettext_lazy as _


# TODO: check if this is set in settings
NAVIGATION_TYPE_CHOICES = (
    ('primary_links', _('primary links')),
    ('secondary_links', _('secondary links')),
)

def register(cls, admin_cls):
    cls.add_to_class('navigation_type', models.CharField(_('navigation type'),
        max_length=32, choices=NAVIGATION_TYPE_CHOICES))
