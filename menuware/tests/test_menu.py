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

    def test_staff(self):
        self.request.user = StaffUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_staff)
        self.assertFalse(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_superuser(self):
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

    def test_is_true(self):
        self.assertTrue(self.menu.is_true({'foo': True}, 'foo'))
        self.assertFalse(self.menu.is_true({'foo': False}, 'foo'))
        self.assertFalse(self.menu.is_true({'foo': True}, 'bar'))

    def test_show_to_all(self):
        self.assertFalse(self.menu.show_to_all({}))
        self.assertFalse(self.menu.show_to_all({'pre_login_visible': False}))
        self.assertFalse(self.menu.show_to_all({'post_login_visible': False}))
        self.assertFalse(self.menu.show_to_all({'pre_login_visible': True}))
        self.assertFalse(self.menu.show_to_all({'pre_login_visible': True, 'post_login_visible': False}))
        self.assertTrue(self.menu.show_to_all({'pre_login_visible': True, 'post_login_visible': True}))

    def test_show_to_authenticated_users(self):
        self.request.user = RegularUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.show_to_authenticated({}))
        self.assertFalse(self.menu.show_to_authenticated({'post_login_visible': False}))
        self.assertFalse(self.menu.show_to_authenticated({'post_login_visible': True}))

        self.request.user = AuthenticatedUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.show_to_authenticated({}))
        self.assertFalse(self.menu.show_to_authenticated({'post_login_visible': False}))
        self.assertTrue(self.menu.show_to_authenticated({'post_login_visible': True}))

    def test_show_to_unauthenticated_users(self):
        self.request.user = RegularUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.show_to_unauthenticated({}))
        self.assertFalse(self.menu.show_to_unauthenticated({'pre_login_visible': False}))
        self.assertTrue(self.menu.show_to_unauthenticated({'pre_login_visible': True}))

        self.request.user = AuthenticatedUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.show_to_unauthenticated({}))
        self.assertFalse(self.menu.show_to_unauthenticated({'pre_login_visible': False}))
        self.assertFalse(self.menu.show_to_unauthenticated({'pre_login_visible': True}))

    def test_is_superuser_safe(self):
        self.request.user = RegularUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_superuser_safe({}))
        self.assertTrue(self.menu.is_superuser_safe({'superuser_required': False}))
        self.assertFalse(self.menu.is_superuser_safe({'superuser_required': True}))

        self.request.user = SuperUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_superuser_safe({'superuser_required': True}))

    def test_is_staff_safe(self):
        self.request.user = RegularUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_staff_safe({}))
        self.assertTrue(self.menu.is_staff_safe({'staff_required': False}))
        self.assertFalse(self.menu.is_staff_safe({'staff_required': True}))

        self.request.user = StaffUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_staff_safe({'staff_required': True}))

    def test_get_url(self):
        self.assertEqual(self.menu.get_url({}), '')
        self.assertEqual(self.menu.get_url({'url': '/'}), '/')
        self.assertEqual(self.menu.get_url({'url': '/foo/bar'}), '/foo/bar')
        self.assertEqual(self.menu.get_url({'url': 'named_url'}), 'named_url')

    def test_has_url(self):
        self.assertFalse(self.menu.has_url({}))
        self.assertTrue(self.menu.get_url({'url': '/'}))
        self.assertTrue(self.menu.get_url({'url': '/foo/bar'}))
        self.assertTrue(self.menu.get_url({'url': 'named_url'}))

    def test_get_menu_list(self):
        self.request.user = RegularUser()
        self.menu.save_user_state(self.request)
        list_dict = [
            {
                "name": "Main Page",
                "url": "/",
                "pre_login_visible": True,
                "post_login_visible": True,
                "superuser_required": False,
                "staff_required": False,
                "selected": False
            },
            {
                "name": "About Page",
                "url": "/about/",
                "pre_login_visible": True,
                "post_login_visible": True,
                "superuser_required": False,
                "staff_required": False,
                "selected": False
            },
            {
                "name": "Account Page",
                "url": "/account/",
                "pre_login_visible": False,
                "post_login_visible": True,
                "superuser_required": False,
                "staff_required": False,
                "selected": False
            },
        ]
        visible = 0
        for item in self.menu.get_menu_list(list_dict):
            visible += 1
        self.assertEqual(visible, 2)

        self.request.user = AuthenticatedUser()
        self.menu.save_user_state(self.request)
        visible = 0
        for item in self.menu.get_menu_list(list_dict):
            visible += 1
        self.assertEqual(visible, 3)

        list_dict.append({
            "name": "Admin Page",
            "url": "/admin/",
            "pre_login_visible": False,
            "post_login_visible": True,
            "superuser_required": True,
            "staff_required": False,
            "selected": False
        })
        visible = 0
        for item in self.menu.get_menu_list(list_dict):
            visible += 1
        self.assertEqual(visible, 3)

        self.request.user = SuperUser()
        self.menu.save_user_state(self.request)
        visible = 0
        for item in self.menu.get_menu_list(list_dict):
            visible += 1
        self.assertEqual(visible, 2)

        self.menu.is_authenticated = True
        visible = 0
        for item in self.menu.get_menu_list(list_dict):
            visible += 1
        self.assertEqual(visible, 4)
