from django.core.urlresolvers import reverse
from django import template
from django.conf import settings

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model

from feincms.module.page.models import Page, PageManager


register = template.Library()


def get_navigation(start_page=None, level=0, depth=1, active_depth=0, language=None, navigation_type=None, extended=False):
    if not start_page:
        root = Page.objects
    else:
        if (start_page.level < level - 1):
            return []
        if start_page.is_root_node() or (start_page.level == level-1):
            root_page = start_page
        else:
            root_page = start_page.get_ancestors().get(level=max(level-1, 0))
        root = Page.objects.filter(lft__gte=root_page.lft, rght__lte=root_page.rght, tree_id=root_page.tree_id)
    from_level = level
    to_level = level + depth
    queryset = root.filter(level__gte=from_level, level__lt=to_level, in_navigation=True)
    if language:
        queryset = queryset.filter(language=language)
    if navigation_type:
        queryset = queryset.filter(navigation_type=navigation_type)
    queryset = PageManager.apply_active_filters(queryset)
    entries = list(queryset)
    if start_page and active_depth and (start_page.level >= level):
        active_node = start_page if (start_page.level == level) else start_page.get_ancestors().filter(in_navigation=True).get(level=level)
        # handle case when start_page is not in navigation
        if active_node in entries:
            index = entries.index(active_node) + 1
            entries[index:index] = active_node.children.filter(in_navigation=True).filter(level__lte=level + active_depth)
    if extended:
        _entries = list(entries)
        entries = []
        # add extended navigation from root_page
        if getattr(root_page, 'navigation_extension', None):
            extended_entries = [p for p in root_page.extended_navigation(level=root_page.level+1, 
                                tree_id=root_page.tree_id, lft=0, rght=0) if p.level <= root_page.level+depth]
            entries.extend(extended_entries)        
        # and from all entries
        for entry in _entries:
            entries.append(entry)
            if getattr(entry, 'navigation_extension', None):
                extended_entries = [p for p in entry.extended_navigation(level=entry.level+1, 
                                    tree_id=root_page.tree_id, lft=0, rght=0) if p.level <= root_page.level+depth]
                entries.extend(extended_entries)        
    return entries


@tag(register, [Optional([Constant("for"), Variable("start_page")]), 
                Optional([Constant("level"), Variable("level")]), 
                Optional([Constant("depth"), Variable("depth")]), 
                Optional([Constant("active_depth"), Variable("active_depth")]), 
                Optional([Constant("language"), Variable("language")]), 
                Optional([Constant("type"), Variable("navigation_type")]), 
                Optional([Constant("extended"), Variable("extended")]), 
                Optional([Constant("as"), Name('asvar')])
                ])
def extended_navigation(context, start_page=None, level=0, depth=1, active_depth=0, language=None, navigation_type=None, extended=False, asvar=None):
    if isinstance(start_page, basestring):
        start_page = Page.objects.get(title=start_page)
    entries = get_navigation(start_page=start_page, level=level, 
                depth=depth, active_depth=active_depth, language=language, 
                extended=extended, navigation_type=navigation_type)
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



    
