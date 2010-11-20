from feincmsext.simple_permission.models import PagePermission


class SimplePagePermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False

        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False

        all_parents = list(obj.get_ancestors(True))
        if perm != 'delete':
            all_parents.insert(0, obj)

        permissions = PagePermission.objects.filter(page__in=all_parents,
                                                    user=user_obj)
        for page in all_parents:
            for p in permissions:
                if p.page == page:
                    return p.can(perm)

