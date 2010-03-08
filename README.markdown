Extensions for FeinCMS.
=======================

[FeinCMS](http://github.com/matthiask/feincms)

Example application is bundled.

extended_navigation
-------------------

Adds navigation_type fields to pages.
Depending on the navigation_type, navigation can be splitted, in primary links, secondary links and so on.

There is also extended_navigation template tag that uses mptt tree_info filter to render tree structure.

extended_navigation uses and requires django-templatetag-sugar
http://github.com/alex/django-templatetag-sugar


util
----

Django management command to create structure from text file.

Menu structure file:

	# Home
	## Menu 1
	### Menu 1.1
	## Menu 2
	### Menu 2.1

./manage.py importstructure --delete_all ../menus.txt
./manage.py importstructure --root 1 ../menus.txt
