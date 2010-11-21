from django.contrib import admin

from mptt.forms import TreeNodeChoiceField
from feincms.module.page.models import Page, PageAdmin as OldPageAdmin

from models import PagePermission


class PagePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'page', 'permission')
    list_filter = ('user', 'page')

    def formfield_for_dbfield(self, db_field, **kwargs): 
        if db_field.attname == 'page_id': 
            return TreeNodeChoiceField(queryset = Page.tree.all(), empty_label = "---------")
        return super(PagePermissionAdmin, self).formfield_for_dbfield(db_field, **kwargs)    


class ObjectPermissionMixin(object):
    def has_add_child_permission(self, request, obj):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_add_permission())

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission(), obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission(), obj)


class PageAdmin(ObjectPermissionMixin, OldPageAdmin):
    def queryset(self, request):
        """
        Return queryset without objects that user does not have 'change' permission.
        """
        qs = super(PageAdmin, self).queryset(request)
        opts = self.opts
        perm = opts.app_label + '.' + opts.get_change_permission()
        forbidden = [obj.id for obj in qs if not request.user.has_perm(perm, obj)]
        qs = qs.exclude(id__in=forbidden)
        print qs
        return qs

    # dont display link to add child page
    pass

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
admin.site.register(PagePermission, PagePermissionAdmin)
