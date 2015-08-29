from django.http import HttpRequest
from django.test import TestCase
from ..menu import MenuBase


class RegularUser(object):
    is_staff = False
    is_superuser = False

    def is_authenticated(self):
        return False


class StaffUser(RegularUser):
    is_staff = True


class SuperUser(StaffUser):
    is_superuser = True


class AuthenticatedUser(RegularUser):
    def is_authenticated(self):
        return True


class MenuTestCase(TestCase):
    """
    Menu Test
    """
    def setUp(self):
        self.request = HttpRequest()
        self.request.path = '/'
        self.menu = MenuBase()

    def test_reqular_user(self):
        self.request.user = RegularUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.is_staff)
        self.assertFalse(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_staff_user(self):
        self.request.user = StaffUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_staff)
        self.assertFalse(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_super_user(self):
        self.request.user = SuperUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_staff)
        self.assertTrue(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_authenticated_user(self):
        self.request.user = AuthenticatedUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.is_staff)
        self.assertFalse(self.menu.is_superuser)
        self.assertTrue(self.menu.is_authenticated)
