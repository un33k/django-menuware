from django.http import HttpRequest
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from ..menu import MenuBase
from ..menu import generate_menu
from ..templatetags.menuware import get_menu


def is_user_happy(request):
    return request.user.is_auth and request.user.is_happy


def is_paid_user(request):
    return request.user.is_auth and request.user.is_happy


def is_main_site(request):
    """
    Non-User condition.
    """
    return True


class TestUser(object):
    """
    Test User Object.
    """
    is_auth = False
    is_staff = False
    is_superuser = False
    is_happy = False
    is_paid = False

    def __init__(self, staff=False, superuser=False, authenticated=False, happy=False, paid=False):
        self.is_auth = authenticated
        self.is_staff = authenticated and staff
        self.is_superuser = authenticated and superuser
        self.is_happy = authenticated and happy
        self.is_paid = authenticated and paid

    @property
    def is_authenticated(self):
        return self.is_auth


class MenuTestCase(TestCase):
    """
    Menu Test
    """
    def setUp(self):
        """
        Setup the test.
        """
        self.request = HttpRequest()
        self.request.path = '/'
        self.menu = MenuBase()

    def test_tempalte_tag(self):
        self.request.user = TestUser(authenticated=True)
        ctx = {
            'request': self.request
        }
        nav = get_menu(ctx, 'NAV_MENU')
        self.assertEqual(len(nav), 2)

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

    def test_state_anonymous_user(self):
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertFalse(self.menu.request.user.is_authenticated)

    def test_state_reqular_user(self):
        self.request.user = TestUser(authenticated=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.request.user.is_authenticated)
        self.assertFalse(self.menu.request.user.is_staff)
        self.assertFalse(self.menu.request.user.is_superuser)

    def test_state_staff(self):
        self.request.user = TestUser(authenticated=True, staff=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.request.user.is_staff)

    def test_state_superuser(self):
        self.request.user = TestUser(authenticated=True, superuser=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.request.user.is_superuser)

    def test_menu_is_validated_for_non_list_or_dict_validators(self):
        menu_dict = {
            "validators": "menuware.tests.test_menu.is_main_site",
        }
        try:
            self.assertFalse(self.menu.is_validated(menu_dict))
        except ImproperlyConfigured:
            pass
        else:
            self.fail("Didn't raise ImproperlyConfigured") # pragma: no cover

    def test_menu_is_validated_for_dict_validators(self):
        menu_dict = {
            "validators": ("menuware.tests.test_menu.is_main_site", ),
        }
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_dotted_notiation(self):
        menu_dict = {
            "validators": ["menuware.tests.test_menu.is_main_site"],
        }
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_invalid_dotted_notiation(self):
        menu_dict = {
            "validators": ["foobar.hello"],
        }
        try:
            self.assertTrue(self.menu.is_validated(menu_dict))
        except ImportError:
            pass
        else:
            self.fail("Didn't raise ImportError") # pragma: no cover

    def test_menu_is_validated_callables(self):
        menu_dict = {
            "validators": [is_main_site],
        }
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_without_validators(self):
        menu_dict = {
            # no validators
        }
        self.assertTrue(self.menu.is_validated({}))

    def test_menu_is_validated_for_authenticated_users(self):
        menu_dict = {
            "validators": ["menuware.utils.is_authenticated"],
        }
        self.request.user = TestUser(authenticated=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_for_unauthenticated_users(self):
        menu_dict = {
            "validators": ["menuware.utils.is_anonymous"],
        }
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_for_superusers(self):
        menu_dict = {
            "validators": ["menuware.utils.is_superuser"],
        }
        self.request.user = TestUser(authenticated=True, superuser=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_for_staff(self):
        menu_dict = {
            "validators": ["menuware.utils.is_staff"],
        }
        self.request.user = TestUser(authenticated=True, staff=True)
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_menu_is_validated_for_non_user_specific_conditions(self):
        menu_dict = {
            "validators": ["menuware.tests.test_menu.is_main_site"],
        }
        self.request.user = TestUser()
        self.menu.save_user_state(self.request)
        self.assertTrue(self.menu.is_validated(menu_dict))

    def test_generate_menu_submenu_attribute_inheritance(self):
        self.request.user = TestUser(staff=True, authenticated=True, happy=True)
        self.menu.save_user_state(self.request)
        list_dict = [
            {   # Menu item -- is_saff validator will be applied to the child node
                "name": "parent1",
                "url": "/user/account/",
                "validators": ["menuware.utils.is_staff", ],
                "submenu": [
                    {
                        "name": "child1",
                        "url": '/user/account/profile/',
                    },
                ],
            },
            {   # Menu item -- is_saff validator will be applied to the child node
                "name": "parent2",
                "url": "/user/settings/",
                "validators": ["menuware.utils.is_authenticated", ],
                "submenu": [
                    {
                        "name": "child1",
                        "url": '/user/settings/happy/',
                        "validators": [
                            "menuware.tests.test_menu.is_user_happy",
                        ],
                    },
                    {
                        "name": "child2",
                        "url": '/user/settings/paid/',
                        "validators": [
                            is_paid_user,
                        ],
                    },
                ],
            },
        ]
        nav = self.menu.generate_menu(list_dict)
        self.assertEqual(len(nav), 2)

        self.assertTrue('menuware.utils.is_staff' in nav[0]['validators'])
        self.assertTrue('menuware.utils.is_staff' in nav[0]['submenu'][0]['validators'])

        self.assertTrue('menuware.utils.is_authenticated' in nav[1]['validators'])
        self.assertTrue('menuware.utils.is_authenticated' in nav[1]['submenu'][0]['validators'])
        self.assertTrue('menuware.utils.is_authenticated' in nav[1]['submenu'][1]['validators'])

        self.assertTrue('menuware.tests.test_menu.is_user_happy' in nav[1]['submenu'][0]['validators'])
        self.assertTrue(is_paid_user in nav[1]['submenu'][1]['validators'])
