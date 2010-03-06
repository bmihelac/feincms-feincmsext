from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.module.blog.models import Entry, EntryAdmin
from feincms.module.page.models import Page
from feincms.content.raw.models import RawContent
from feincms.content.image.models import ImageContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.application.models import ApplicationContent
from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender
from feincms.content.application.models import reverse

import mptt

Page.register_templates({
    'key': 'base',
    'title': 'Base Template',
    'path': 'base.html',
    'regions': (
        ('main', 'Main region'),
        ('sidebar', 'Sidebar', 'inherited'),
        ),
    })
Page.create_content_type(RawContent)
MediaFileContent.default_create_content_type(Page)
Page.create_content_type(ImageContent, POSITION_CHOICES=(
    ('default', 'Default position'),
    ))
Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('blog_urls', 'Blog'),
    ))    


Entry.register_regions(
    ('main', 'Main region'),
    )
Entry.create_content_type(RawContent)
Entry.create_content_type(ImageContent, POSITION_CHOICES=(
    ('default', 'Default position'),
    ))
    
    
class BlogEntriesNavigationExtension(NavigationExtension):
    """
    Extended navigation for blog entries.
    
    It would be added to 'Blog' page properties in admin.
    """
    name = _('all blog entries')

    def children(self, page, **kwargs):
        for entry in Entry.objects.all():
            yield PagePretender(
                title=entry.title,
                url=reverse('blog_urls/blog_entry_details', kwargs={'object_id': entry.id}),
                level=kwargs['level'], 
                # NOTE: this is hack, just to make tree_info happy
                tree_id=0, lft=0, rght=0
                )

Page.register_extensions('navigation', 'feincmsext.extended_navigation.extensions.navigation_type')


