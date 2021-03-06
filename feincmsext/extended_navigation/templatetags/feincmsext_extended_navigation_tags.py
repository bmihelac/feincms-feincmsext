from django import template

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional

from feincms.module.page.models import Page, PageManager
from feincms.module.page.extensions.navigation import PagePretender

from feincmsext.extended_navigation.util import regex_group_list


register = template.Library()


def get_navigation(start_page=None, level=0, depth=1, active_depth=0,
        language=None, navigation_type=None, extended=False,
        request=None):
    if not start_page:
        root = Page.objects
    else:
        if (start_page.level < level - 1):
            return []
        if start_page.is_root_node() or (start_page.level == level - 1):
            root_page = start_page
        else:
            root_page = start_page.get_ancestors().get(level=max(level - 1, 0))
        root = Page.objects.filter(lft__gte=root_page.lft,
                rght__lte=root_page.rght, tree_id=root_page.tree_id)
    from_level = level
    to_level = level + depth
    queryset = root.filter(level__gte=from_level,
            level__lt=to_level, in_navigation=True)
    if language:
        queryset = queryset.filter(language=language)
    if navigation_type:
        queryset = queryset.filter(navigation_type=navigation_type)
    queryset = PageManager.apply_active_filters(queryset)
    entries = list(queryset)

    active_node = None
    if start_page and active_depth and (start_page.level >= level):
        if start_page.level == level:
            active_node = start_page
        else:
            try:
                active_node = start_page.get_ancestors().get(
                        in_navigation=True, level=level)
            except type(start_page).DoesNotExist:
                # active_node is not in navigation
                active_node = None
        # handle case when start_page is not in navigation
        if active_node in entries:
            index = entries.index(active_node) + 1
            entries[index:index] = active_node.children.filter(
                    in_navigation=True).filter(level__lte=level + active_depth)

    if extended:
        _entries = list(entries)
        entries = []
        # add extended navigation from root_page
        if getattr(root_page, 'navigation_extension', None):
            extended_entries = [p for p in root_page.extended_navigation(
                level=root_page.level + 1,
                tree_id=root_page.tree_id, lft=0, rght=0,
                request=request) if p.level <= root_page.level + depth]
            entries.extend(extended_entries)
        # and from all entries
        for entry in _entries:
            entries.append(entry)
            max_depth = active_depth if active_node == entry else depth
            if getattr(entry, 'navigation_extension', None):
                extended_entries = [p for p in entry.extended_navigation(
                    level=entry.level + 1,
                    tree_id=root_page.tree_id, lft=0, rght=0,
                    request=request) if p.level <= root_page.level + max_depth]
                entries.extend(extended_entries)
    return entries


@tag(register, [Optional([Constant("for"), Variable("start_page")]),
                Optional([Constant("level"), Variable("level")]),
                Optional([Constant("depth"), Variable("depth")]),
                Optional([Constant("active_depth"), Variable("active_depth")]),
                Optional([Constant("language"), Variable("language")]),
                Optional([Constant("type"), Variable("navigation_type")]),
                Optional([Constant("extended"), Variable("extended")]),
                Optional([Constant("request"), Variable("request")]),
                Optional([Constant("as"), Name('asvar')])
                ])
def extended_navigation(context, start_page=None, level=0, depth=1,
        active_depth=0, language=None, navigation_type=None,
        extended=False, request=None, asvar=None):
    if isinstance(start_page, basestring):
        start_page = Page.objects.get(title=start_page)
    entries = get_navigation(start_page=start_page, level=level,
                depth=depth, active_depth=active_depth, language=language,
                extended=extended, navigation_type=navigation_type,
                request=request)
    if asvar:
        context[asvar] = entries
        return ""
    else:
        arr = []
        arr.append('<ul>')
        for page in entries:
            arr.append('<li><a href="%s">%s</a></li>' % (
                page.get_absolute_url(), page.title))
        arr.append('</ul>')
        return '\n'.join(arr)


@tag(register, [Constant("for"), Variable("start_page"),
                Constant("level"), Variable("level"),
                Constant("as"), Name('asvar')
                ])
def parent_feincms_page(context, start_page, level, asvar):
    """Get parent page for given level in tree hierarchy."""
    if not start_page or start_page.level < level:
        context[asvar] = None
        return ""
    if start_page.level == level:
        context[asvar] = start_page
        return ""
    context[asvar] = start_page.get_ancestors()[level]
    return ""


@tag(register, [Variable("contents"),
                Variable("expr"),
                Constant("as"), Name('asvar')
                ])
def group_page_content(context, contents, expr, asvar):
    """
    Allows grouping feincms page contents with regular expressions.

        {% group_page_content feincms_page.content.main "[richtext]{2}"
        as content_groups %}

    """
    context[asvar] = regex_group_list(contents,
            expr,
            lambda x: x._meta.module_name)
    return ''


@register.assignment_tag
def is_equal_or_parent_or_pretender(page1, page2, request):
    """
    Determines whether a given page is equal to or the parent of another
    page.

    If ``page1`` is ``Page`` object, compare mptt tree (this is same as
    FeinCMS ``is_equal_or_parent_of`` filter functionality).

    However, if ``page1`` is PagePretender, return if `page1` is contained in
    current url.
    """
    if not isinstance(page1, PagePretender):
        return (page1.tree_id == page2.tree_id
                and page1.lft <= page2.lft
                and page1.rght >= page2.rght)
    url = request.META['PATH_INFO']
    return page1.get_absolute_url() in url
