import re

from django.template.defaultfilters import slugify

from feincms.module.page.models import Page


def import_structure(f, root_id=None):
    """docstring for import_structure"""
    parents = {}
    if root_id:
        parents[0] = Page.objects.get(id=root_id)
    else:
        parents[0] = None
        
    for line in f:
        match = re.match(r"^(#+) (.*)$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2) 
            p = Page(active=True, title=title, slug=slugify(title), in_navigation=True, parent=parents[level-1])
            p.save()
            parents[level] = p
            print ('adding FeinCMS page: %s' % title)
