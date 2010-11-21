Extensions for FeinCMS.
=======================

Various **experimental** tools and modules for [FeinCMS](http://github.com/matthiask/feincms).

Example application is bundled (run ./setup_symlinks.py inside example folder to symlink FeinCMS media files.

extended_navigation
-------------------

Adds navigation_type fields to pages.
Depending on the navigation_type, navigation can be splitted, in primary links, secondary links and so on.

Navigation types can be defined in settings

	NAVIGATION_TYPE_CHOICES = (
	    ('primary_links', _('primary links')),
	    ('secondary_links', _('secondary links')),
	)

extended_navigation template tag, together with mptt tree_info template filter renders tree structure.

extended_navigation uses and requires django-templatetag-sugar
http://github.com/alex/django-templatetag-sugar

group_page_content
------------------

group_page_content templatetag allows more complex layouts by grouping page contents with regular expressions, here are some examples:

Wrap image content in div, but if it is followed by textcontent group them together under the same div:

  {% group_page_content feincms_page.content.main "[imagecontent][rawcontent]?" as content_groups %}

Group 2 successive text contents together in newsletter like columns:

  {% group_page_content feincms_page.content.main "[rawcontent]{2}" as content_groups %}
  
-![group_page_content screenshot](http://github.com/bmihelac/feincms-feincmsext/raw/master/example/media/regroup-content-example.jpg)


util
----

Django management command to create structure from text file.

Menu structure file:

	# Home
	## Menu 1
	### Menu 1.1
	## Menu 2
	### Menu 2.1

This would delete ALL EXISTING PAGES and create structure from file:

	./manage.py importstructure --delete_all menus.txt
	
And this would add structure from the text file to page with id of 1:

	./manage.py importstructure --root 1 menus.txt

simple permissions
------------------

For any page, following permissions can be set.

* none - user cannot do anything
* change - user can edit selected page and all childrent pages
* all - user can edit all pages in subtree, add new pages or delete them. User cannot remove selected page.

To add simple permission, add 'feincmsext.simple_permission' to INSTALLED_APPS and update AUTHENTICATION_BACKENDS with:

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'feincmsext.simple_permission.backend.SimplePagePermissionBackend',
    )

simple permissions are implemented in example app for user1 (pass)
