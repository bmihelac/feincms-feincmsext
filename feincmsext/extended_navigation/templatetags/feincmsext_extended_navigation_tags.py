from django.core.urlresolvers import reverse
from django import template
from django.conf import settings

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model

from feincms.module.page.models import Page, PageManager


register = template.Library()


def get_navigation(start_page=None, level=0, depth=1, language=None, navigation_type=None, extended=False):
    if not start_page:
        root = Page.objects
        start_level = 0
    else:
        root = start_page.get_descendants()
        start_level = start_page.level + 1
    from_level = start_level + level
    to_level = start_level + level + depth
    queryset = root.filter(level__gte=from_level, level__lt=to_level, in_navigation=True)
    # import pdb; pdb.set_trace()
    if language:
        queryset = queryset.filter(language=language)
    if navigation_type:
        queryset = queryset.filter(navigation_type=navigation_type)
    queryset = PageManager.apply_active_filters(queryset)
    entries = list (queryset)
    if extended:
        _entries = list(entries)
        entries = []
        for entry in _entries:
            entries.append(entry)
            if getattr(entry, 'navigation_extension', None):
                entries.extend(entry.extended_navigation(level=entry.level + 1, tree_id=entry.tree_id, 
                                lft=0, rght=0))        
    return entries


@tag(register, [Optional([Constant("for"), Variable("start_page")]), 
                Optional([Constant("level"), Variable("level")]), 
                Optional([Constant("depth"), Variable("depth")]), 
                Optional([Constant("language"), Variable("language")]), 
                Optional([Constant("type"), Variable("navigation_type")]), 
                Optional([Constant("extended"), Variable("extended")]), 
                Optional([Constant("as"), Name('asvar')])
                ])
def extended_navigation(context, start_page=None, level=0, depth=1, language=None, navigation_type=None, extended=False, asvar=None):
    if isinstance(start_page, basestring):
        start_page = Page.objects.get(title=start_page)
    entries = get_navigation(start_page=start_page, level=level, 
                depth=depth, language=language, extended=extended, navigation_type=navigation_type)
    if asvar:
        context[asvar] = entries
        return ""
    else:
        arr = []
        arr.append('<ul>')
        for page in entries:
            arr.append('<li><a href="%s">%s</a></li>' % (page.get_absolute_url(), page.title))
        arr.append('</ul>')
        return '\n'.join(arr)



    
