from django import template

register = template.Library()


@register.filter
def page_search_result(page):
    """
    Return content in main region for display in search result.
    """
    return "".join([c.render() for c in page.content.main])


@register.filter
def search_include(result):
    """
    Returns filename to use for search inclusion template for ``result`` object.
    """
    ct = result.content_type()
    args = ct.split('.')
    template_name = "search/_%s_%s.html" % tuple(args)
    return template_name

