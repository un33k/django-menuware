from django.http import HttpRequest
from django.test import TestCase
from ..menu import MenuBase
from ..menu import generate_menu


class TestUser(object):
    is_auth = False
    is_staff = False
    is_superuser = False

    def __init__(self, staff=False, superuser=False, authenticated=False):
        self.is_staff = staff
        self.is_superuser = superuser
        self.is_auth = authenticated

    def is_authenticated(self):
        return self.is_auth


class MenuTestCase(TestCase):
    """
    Menu Test
    """
    def setUp(self):
        self.request = HttpRequest()
        self.request.path = '/'
        self.menu = MenuBase()
        self.list_dict = [
            {   # Menu item -- invisible without a valid `name` attribute
                "url": "/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Menu item -- invisible with a black `name`
                "name": "",
                "url": "/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Menu item -- invisible without a valid `url` attribute
                "name": "No URL Malformed Entry",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Menu item -- invisible without at least one auth render option
                "name": "Main",
                "url": "/",
            },
            {   # Menu item -- visible to anyone, anytime
                "name": "Main",
                "url": "/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
                "submenu": [
                    {
                        "name": "submenu",
                        "url": '/submenu/',
                    },
                ],
            },
            {   # Menu item -- visible to unauthenticated users only
                "name": "Login",
                "url": "admin:login",
                "render_for_unauthenticated": True,
            },
            {   # Menu item -- visible to authenticated users only
                "name": "Logout",
                "url": "/user/logout/",
                "render_for_authenticated": True,
            },
            {   # Menu item -- visible to authenticated staff only
                "name": "Limited Staff Account Access",
                "url": "/user/account/",
                "render_for_authenticated": True,
                "render_for_staff": True,
                "submenu": [
                    {
                        "name": "Profile",
                        "url": '/user/account/profile/',
                    },
                ],
            },
            {   # Menu item -- visible to authenticated superusers only
                "name": "Full Superuser Account Access",
                "url": "/admin/",
                "render_for_authenticated": True,
                "render_for_superuser": True,
            },
        ]

    def test_reqular_user(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.is_staff)
        self.assertFalse(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_staff(self):
        self.request.user = TestUser(staff=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_staff)
        self.assertFalse(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_superuser(self):
        self.request.user = TestUser(superuser=True)
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.is_staff)
        self.assertTrue(self.menu.is_superuser)
        self.assertFalse(self.menu.is_authenticated)

    def test_authenticated_user(self):
        self.request.user = TestUser(authenticated=True)
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
        self.assertFalse(self.menu.show_to_all({'render_for_unauthenticated': False}))
        self.assertFalse(self.menu.show_to_all({'render_for_authenticated': False}))
        self.assertFalse(self.menu.show_to_all({'render_for_unauthenticated': True}))
        self.assertFalse(self.menu.show_to_all({'render_for_unauthenticated': True, 'render_for_authenticated': False}))
        self.assertTrue(self.menu.show_to_all({'render_for_unauthenticated': True, 'render_for_authenticated': True}))

    def test_show_to_authenticated_users(self):
        self.request.user = TestUser(authenticated=True)
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.show_to_authenticated({}))
        self.assertFalse(self.menu.show_to_authenticated({'render_for_authenticated': False}))
        self.assertTrue(self.menu.show_to_authenticated({'render_for_authenticated': True}))

    def test_show_to_unauthenticated_users(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.show_to_unauthenticated({}))
        self.assertFalse(self.menu.show_to_unauthenticated({'render_for_unauthenticated': False}))
        self.assertTrue(self.menu.show_to_unauthenticated({'render_for_unauthenticated': True}))

    def test_show_to_superuser(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.show_to_superuser({}))
        self.assertTrue(self.menu.show_to_superuser({'render_for_superuser': False}))
        self.assertFalse(self.menu.show_to_superuser({'render_for_superuser': True}))

        self.request.user = TestUser(superuser=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.show_to_superuser({'render_for_superuser': True}))

    def test_show_to_staff(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.show_to_staff({}))
        self.assertTrue(self.menu.show_to_staff({'render_for_staff': False}))
        self.assertFalse(self.menu.show_to_staff({'render_for_staff': True}))

        self.request.user = TestUser(staff=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.show_to_staff({'render_for_staff': True}))

    def test_has_name(self):
        self.assertFalse(self.menu.has_name({}))
        self.assertFalse(self.menu.has_name({'name': ''}))
        self.assertTrue(self.menu.has_name({'name': 'Some Name'}))

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

    def test_get_menu_list_anonymous_user(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        nav_count_for_anonymous_user = 0
        for item in self.menu.get_menu_list(self.list_dict):
            nav_count_for_anonymous_user += 1
        self.assertEqual(nav_count_for_anonymous_user, 2)

    def test_get_menu_list_authenticated_user(self):
        self.request.user = TestUser(authenticated=True)
        self.menu.save_user_state(self.request)
        nav_count_for_authenticated_user = 0
        for item in self.menu.get_menu_list(self.list_dict):
            nav_count_for_authenticated_user += 1
        self.assertEqual(nav_count_for_authenticated_user, 2)

    def test_get_menu_list_staff_user(self):
        self.request.user = TestUser(staff=True, authenticated=True)
        self.menu.save_user_state(self.request)
        nav_count_for_staff_user = 0
        for item in self.menu.get_menu_list(self.list_dict):
            nav_count_for_staff_user += 1
        self.assertEqual(nav_count_for_staff_user, 3)

    def test_get_menu_list_superuser(self):
        self.request.user = TestUser(superuser=True, authenticated=True)
        self.menu.save_user_state(self.request)
        nav_count_for_superuser = 0
        for item in self.menu.get_menu_list(self.list_dict):
            nav_count_for_superuser += 1
        self.assertEqual(nav_count_for_superuser, 3)

    def test_generate_menu_anonymous_user(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        nav_count_for_anonymous_user = self.menu.generate_menu(self.list_dict)
        self.assertEqual(len(nav_count_for_anonymous_user), 2)

    def test_generate_menu_authenticated_user(self):
        self.request.user = TestUser(authenticated=True)
        self.menu.save_user_state(self.request)
        nav_count_for_authenticated_user = self.menu.generate_menu(self.list_dict)
        self.assertEqual(len(nav_count_for_authenticated_user), 2)

    def test_generate_menu_staff_user(self):
        self.request.user = TestUser(staff=True, authenticated=True)
        self.menu.save_user_state(self.request)
        nav_count_for_staff_user = self.menu.generate_menu(self.list_dict)
        self.assertEqual(len(nav_count_for_staff_user), 3)

    def test_generate_menu_superuser(self):
        self.request.user = TestUser(superuser=True, authenticated=True)
        self.menu.save_user_state(self.request)
        nav_count_for_superuser = self.menu.generate_menu(self.list_dict)
        self.assertEqual(len(nav_count_for_superuser), 3)

    def test_generate_menu_anonymous_user_callable(self):
        self.request.user = TestUser()
        nav_count_for_anonymous_user = generate_menu(self.request, self.list_dict)
        self.assertEqual(len(nav_count_for_anonymous_user), 2)

    def test_generate_menu_authenticated_user_callable(self):
        self.request.user = TestUser(authenticated=True)
        nav_count_for_authenticated_user = generate_menu(self.request, self.list_dict)
        self.assertEqual(len(nav_count_for_authenticated_user), 2)

    def test_generate_menu_staff_user_callable(self):
        self.request.user = TestUser(staff=True, authenticated=True)
        nav_count_for_staff_user = generate_menu(self.request, self.list_dict)
        self.assertEqual(len(nav_count_for_staff_user), 3)

    def test_generate_menu_superuser_callable(self):
        self.request.user = TestUser(superuser=True, authenticated=True)
        nav_count_for_superuser = generate_menu(self.request, self.list_dict)
        self.assertEqual(len(nav_count_for_superuser), 3)

    def test_generate_menu_submenu_attribute_inheritance(self):
        self.request.user = TestUser(staff=True, authenticated=True)
        self.menu.save_user_state(self.request)
        list_dict = [
            {   # Menu item -- visible to authenticated staff only
                "name": "parent",
                "url": "/user/account/",
                "render_for_authenticated": True,
                "render_for_staff": True,
                "submenu": [
                    {
                        "name": "child",
                        "url": '/user/account/profile/',
                    },
                ],
            },
        ]
        nav = self.menu.generate_menu(list_dict)
        self.assertEqual(len(nav), 1)
        self.assertEqual(nav[0]['render_for_authenticated'],
            nav[0]['submenu'][0]['render_for_authenticated'])
        self.assertEqual(nav[0]['render_for_staff'],
            nav[0]['submenu'][0]['render_for_staff'])
