Extensions for FeinCMS.
=======================

Various tools and modules for [FeinCMS](http://github.com/matthiask/feincms).

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

This would delete ALL EXISTING PAGES and create structure ad is in file:

	./manage.py importstructure --delete_all ../menus.txt
	
And this would add structure from the text file to page with id of 1:

	./manage.py importstructure --root 1 ../menus.txt
