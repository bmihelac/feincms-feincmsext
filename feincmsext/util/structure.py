import re
import json

from django.template.defaultfilters import slugify

from feincms.module.page.models import Page


def import_structure(f, root_id=None):
    """docstring for import_structure"""
    parents = {}
    if root_id:
        parents[0] = Page.objects.get(id=root_id)
    else:
        parents[0] = None
    kwargs = {
        'active': True,
        'in_navigation': True,
    }
    for line in f:
        match = re.match(r"^(#+) (\{[^)]*} )?(.*)$", unicode(line))
        if match:
            level = len(match.group(1))
            opts = match.group(2)
            if opts:
                js = json.loads(opts)
                kwargs.update(**dict([(str(k), v) for k, v in js.items()]))
            title = match.group(3)
            parent = parents[level-1]
            parent_page = Page.objects.get(pk=parent.pk) if parent else None
            p = Page(
                title=title,
                slug=slugify(title),
                parent=parent_page,
                **kwargs
            )
            for field in ('navigation_type',):
                if parent and parent.__dict__.get(field, None):
                    p.__dict__[field] = parent.__dict__[field]
            p.save()
            parents[level] = p
            print('adding FeinCMS page: %s' % title)
