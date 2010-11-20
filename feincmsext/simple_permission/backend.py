from django.contrib.contenttypes.models import ContentType

from feincmsext.simple_permission.models import SimplePermission


class SimplePermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False

        ct = ContentType.objects.get_for_model(obj)

        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False

        all_parents = list(obj.get_ancestors(True))
        if perm != 'delete':
            all_parents.insert(0, obj)
        all_parents_ids = [o.id for o in all_parents]
        permissions = SimplePermission.objects.filter(content_type=ct,
                                           object_id__in=all_parents_ids,
                                           user=user_obj)
        for object_id in all_parents_ids:
            for p in permissions:
                if p.object_id == object_id:
                    return p.can(perm)

