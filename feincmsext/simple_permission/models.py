from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

PERMISSION_CHOICES = (
        ('none', _('none')),
        ('change', _('change items in subtree')),
        ('all', _('change subtree, add and remove items'))
        )
class SimplePermission(models.Model):
    user = models.ForeignKey(User)
    permission = models.CharField(max_length=12, blank=False, choices=PERMISSION_CHOICES)
    can_change = models.BooleanField()
    can_add_delete = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def can(self, action):
        if self.permission == 'none':
            return False
        if action in ('delete', 'add'):
            allowed = (self.permission == 'all')
        else:
            allowed = True
        return allowed
