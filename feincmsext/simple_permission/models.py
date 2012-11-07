from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from feincms.module.page.models import Page


PERMISSION_CHOICES = (
        ('none', _('none')),
        ('change', _('edit subtree')),
        ('all', _('edit, add and remove subtree items'))
        )

class SimplePermissionBase(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    permission = models.CharField(max_length=12, blank=False, 
            choices=PERMISSION_CHOICES,
            verbose_name=_('Permission'))
    
    class Meta:
        abstract=True

    def can(self, action):
        if self.permission == 'none':
            return False
        if action in ('delete', 'addchild'):
            allowed = (self.permission == 'all')
        elif action == 'change':
            allowed = True
        else:
            allowed = False
        return allowed


class PagePermission(SimplePermissionBase):
    page = models.ForeignKey(Page, verbose_name=_('Page'))

    def __unicode__(self):
        return '%s: %s - %s' % (self.user.username, self.permission, self.page)

    class Meta:
        verbose_name = _("Page Permission")
        verbose_name_plural = _("Page Permissions")

