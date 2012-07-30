from django.db.models.fields import FieldDoesNotExist
from haystack import indexes, site

from feincms.module.page.models import Page


class PageIndex(indexes.SearchIndex):
    """
    Index for FeinCMS Page objects.
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='title', boost=1.2)
    content_auto = indexes.EdgeNgramField(model_attr='title')
    url = indexes.CharField(model_attr="_cached_url")
    try:
        Page._meta.get_field_by_name('language')
        language = indexes.CharField(model_attr='language')
    except FieldDoesNotExist:
        pass
    try:
        Page._meta.get_field_by_name('site')
        site = indexes.IntegerField(model_attr='site__id')
    except FieldDoesNotExist:
        pass

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Page.objects.active()


site.register(Page, PageIndex)
