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

group_page_content templatetag allows more complex layouts by grouping page contents with regular expressions. 
Here are some examples:

Wrap image content in div, but if it is followed by textcontent group them together under the same div:

    {% group_page_content feincms_page.content.main "[imagecontent][rawcontent]?" as content_groups %}
  
This will return group list, each group will contain ``name``, ``contents`` tuple. 
Name is by integer with value of 0 for 1st match, 1 for 2nd, etc. Groups that were not listed in expression
would have value -1.

You can also give groups a name:

    {% group_page_content feincms_page.content.main "<myname>[imagecontent][rawcontent]?" as content_groups %}

Group 2 successive text contents together in newsletter like columns:

    {% group_page_content feincms_page.content.main "[rawcontent]{2}" as content_groups %}
  
-![group_page_content screenshot](http://github.com/bmihelac/feincms-feincmsext/raw/master/example/media/regroup-content-example.jpg)

Separate multiple groups with a slash ``/``:

    {% group_page_content feincms_page.content.main "[imagecontent][rawcontent]? / [rawcontent][imagecontent]?" as content_groups %}


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

Notes:
* Delete selected pages action does not check permissions (it uses QuerySet.delete())
* Add child page link is always displayed regardless if page can be added or not

simple permissions are implemented in example app for user1 (pass)

create_content_types
--------------------

Create content types for given ``content_types_conf``.

``content_types_conf`` is a list or tuple, each element should have
content type configuration. 

Content type configuration is list or tuple with following elements:

* content_type - class path or model (can be list)
* region - region (optional, can be list)
* options - dictionary to pass as options (optional)

        >>> content_types = [
                (RichTextContent, ), # all regions
                (
                    ('feincms.content.video.models', MediaFileContent), # multiple content types
                    ('main', 'sidebar'), # multiple regions
                    {'TYPE_CHOICES': (('block', 'block'),), # options
                )
                ]
        >>> create_content_type(Page, content_types)


