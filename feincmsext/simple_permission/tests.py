from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from feincms.module.page.models import Page

from feincmsext.simple_permission.models import PagePermission


class PagePermissionBackendTest(TestCase):
    """
    Tests for auth backend that supports object level permissions
    """
    backend = 'feincmsext.simple_permission.backend.SimplePagePermissionBackend'

    def setUp(self):
        self.curr_auth = settings.AUTHENTICATION_BACKENDS
        settings.AUTHENTICATION_BACKENDS = tuple(self.curr_auth) + (self.backend,)
        self.user1 = User.objects.create_user('test', 'test@example.com', 'test')
        self.user2 = User.objects.create_user('test2', 'test2@example.com', 'test')
        self.page_1 = Page.objects.create(title='1', slug='1', parent=None)
        self.page_1_1 = Page.objects.create(title='1.1', slug='1.1', parent=self.page_1)
        self.page_1 = Page.objects.get(pk=self.page_1.id)
        self.page_1_1_1 = Page.objects.create(title='1.1.1', slug='1.1.1', parent=self.page_1_1)
        self.page_1 = Page.objects.get(pk=self.page_1.id)
        self.page_1_1 = Page.objects.get(pk=self.page_1_1.id)
        self.page_1_2 = Page.objects.create(title='1.2', slug='1.2', parent=self.page_1)
        self.page_1 = Page.objects.get(pk=self.page_1.id)
        self.page_1_3 = Page.objects.create(title='1.3', slug='1.3', parent=self.page_1)

    def tearDown(self):
        settings.AUTHENTICATION_BACKENDS = self.curr_auth

    def add_permission(self, user, page, permission):
        PagePermission.objects.create(user=user, 
                permission=permission,
                page=page)

    def test_has_perm(self):
        self.add_permission(self.user1, self.page_1, 'change')
        self.assertEqual(self.user1.has_perm('page.change_page', self.page_1), True)
        self.assertEqual(self.user1.has_perm('page.change_page', self.page_1_1), True)
        self.assertEqual(self.user1.has_perm('page.change_page', self.page_1_1_1), True)
        self.assertEqual(self.user1.has_perm('page.delete_page', self.page_1_1_1), False)
        self.assertEqual(self.user1.has_perm('page.addchild_page', self.page_1_1_1), False)
        self.assertEqual(self.user2.has_perm('page.change_page', self.page_1), False)

        self.add_permission(self.user2, self.page_1_1, 'all')
        self.assertEqual(self.user2.has_perm('page.change_page', self.page_1), False)
        self.assertEqual(self.user2.has_perm('page.change_page', self.page_1_1), True)
        self.assertEqual(self.user2.has_perm('page.delete_page', self.page_1_1), False)
        self.assertEqual(self.user2.has_perm('page.delete_page', self.page_1_1_1), True)
        self.assertEqual(self.user2.has_perm('page.addchild_page', self.page_1_1_1), True)
