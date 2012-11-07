from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField
from feincms.module.page.models import Page, PageAdmin as OldPageAdmin

from models import PagePermission


class PagePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'page', 'permission')
    list_filter = ('user', 'page')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname == 'page_id':
            return TreeNodeChoiceField(queryset=Page.objects.all(),
                    empty_label="---------", label=_('Page'))
        return super(PagePermissionAdmin,
                self).formfield_for_dbfield(db_field, **kwargs)


class ObjectPermissionMixin(object):
    def has_add_child_permission(self, request, obj):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.addchild_page', obj)

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission(), obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission(), obj)

    def queryset(self, request):
        """
        Return queryset without objects that user does not have 'change' permission.
        """
        qs = super(ObjectPermissionMixin, self).queryset(request)
        opts = self.opts
        perm = opts.app_label + '.' + opts.get_change_permission()
        forbidden = [obj.id for obj in qs if not request.user.has_perm(perm, obj)]
        qs = qs.exclude(id__in=forbidden)
        return qs

    def _actions_column(self, page):
        """
        see #13659 http://code.djangoproject.com/ticket/13659
        When this patch is applied we could check if user is allowed to 
        add child pages and show/hide link in respect to this.
        """
        actions = super(ObjectPermissionMixin, self)._actions_column(page)
        #request = None
        #if self.has_add_child_permission(request, page):
        #    actions.pop(1)
        return actions

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.pk:
            if not obj.parent or not self.has_add_child_permission(request, obj.parent):
                raise PermissionDenied
        obj.save()



class PageAdmin(ObjectPermissionMixin, OldPageAdmin):
    actions = None

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
admin.site.register(PagePermission, PagePermissionAdmin)
