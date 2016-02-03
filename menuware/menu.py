import copy

from importlib import import_module

from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch


class MenuBase(object):
    """
    Base class that generates menu list.
    """
    def __init__(self):
        self.path = ''
        self.request = None
        self.is_staff = False
        self.is_superuser = False
        self.is_authenticated = False
        self.inheritable_attributes = [
            'render_for_staff',
            'render_for_superuser',
            'render_for_authenticated',
            'render_for_unauthenticated',
            'render_for_user_when_condition_is_true',
        ]

    def save_user_state(self, request):
        """
        Given a request object, store the current user attributes
        """
        self.request = request
        self.path = request.path
        self.is_staff = request.user.is_staff
        self.is_superuser = request.user.is_superuser
        self.is_authenticated = request.user.is_authenticated()

    def is_true(self, item_dict, key):
        """
        Given a menu item dictionary, and a key, it returns True if key is set to True
        else returns False
        """
        yep = item_dict.get(key, False)
        return yep

    def show_to_all(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be shown
        for both authenticated and unauthenticated users. (e.g. a `contact` menu item)
        """
        show = self.is_true(item_dict, 'render_for_unauthenticated') and \
            self.is_true(item_dict, 'render_for_authenticated')
        return show

    def show_to_user_if_condition_is_true(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to users if a set condition is true. (e.g. show if user is remember of admin group)
        """
        condition_check_path = item_dict.get('render_for_user_when_condition_is_true')
        if condition_check_path is None:
            return True

        condition_check_module = '.'.join(condition_check_path.split('.')[:-1])
        condition_check_procedure = condition_check_path.split('.')[-1]
        condition_check_module = import_module(condition_check_module)
        condition_check_procedure = getattr(condition_check_module, condition_check_procedure)

        if condition_check_procedure is None:
            return False

        show = condition_check_procedure(self.request)
        return show

    def show_to_authenticated(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to authenticated users. (e.g. a `logout` menu item)
        """
        show = self.is_true(item_dict, 'render_for_authenticated') and self.is_authenticated
        return show

    def show_to_unauthenticated(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to unauthenticated users. (e.g. a `login` menu item)
        """
        show = self.is_true(item_dict, 'render_for_unauthenticated') and not self.is_authenticated
        return show

    def show_to_superuser(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to super users. (e.g. a `admin` menu item)
        """
        yep = True
        if self.is_true(item_dict, 'render_for_superuser') and not self.is_superuser:
            yep = False
        return yep

    def show_to_staff(self, item_dict):
        """
        Given a menu item dictionary, it returns true if menu item should be only shown
        to staff users. (e.g. a `limited admin` menu item)
        """
        yep = True
        if self.is_true(item_dict, 'render_for_staff') and not self.is_staff:
            yep = False
        return yep

    def has_name(self, item_dict):
        """
        Given a menu item dictionary, it returns true if attribute `name` is set.
        """
        yep = True
        if not item_dict.get('name', False):
            yep = False
        return yep

    def get_url(self, item_dict):
        """
        Given a menu item dictionary, it returns the URL or an empty string.
        """
        final_url = ''
        url = item_dict.get('url', '')
        try:
            final_url = reverse(url)
        except NoReverseMatch:
            final_url = url
        return final_url

    def has_url(self, item_dict):
        """
        Given a menu item dictionary, it returns true if attribute `url` is set.
        """
        if not self.get_url(item_dict):
            return False
        return True

    def is_selected(self, item_dict):
        """
        Given a menu item dictionary, it returns true if `url` is on path.
        """
        url = self.get_url(item_dict)
        if len(url) and url == self.path:
            return True
        return False

    def process_breadcrums(self, menu_list):
        """
        Given a menu list, it marks the items on the current path as selected, which
        can be used as breadcrumbs
        """
        for item in menu_list:
            if item['submenu']:
                item['selected'] = self.process_breadcrums(item['submenu'])
            if item['selected']:
                return True
        return False

    def copy_attributes(self, parent_dict, child_dict, attrs):
        """
        Given a list of attribute, it copies the same attributes from the parent
        dict to the child dict.
        """
        for attr in attrs:
            has_attr = parent_dict.get(attr)
            if has_attr is not None:
                child_dict[attr] = has_attr

    def get_submenu_list(self, parent_dict, depth):
        """
        Given a menu item dictionary, it returns a submenu if one exist, or
        returns None.
        """
        submenu = parent_dict.get('submenu', None)
        if submenu is not None:
            for child_dict in submenu:
                self.copy_attributes(parent_dict, child_dict, self.inheritable_attributes)
            submenu = self.generate_menu(submenu, depth)
            if not submenu:
                submenu = None
        return submenu

    def get_menu_list(self, list_dict):
        """
        A generator that returns only the visible menu items.
        """
        for item in list_dict:
            if not self.has_name(item) or not self.has_url(item):
                continue
            if self.show_to_all(item):
                pass
            elif self.show_to_authenticated(item):
                pass
            elif self.show_to_unauthenticated(item):
                pass
            else:
                continue
            if not self.show_to_user_if_condition_is_true(item):
                continue
            if not self.show_to_superuser(item):
                continue
            if not self.show_to_staff(item):
                continue
            yield copy.copy(item)

    def generate_menu(self, list_dict, depth=None):
        """
        Given a list of dictionaries, returns a menu list.
        """
        visible_menu = []
        current_depth = depth or 0
        for item in self.get_menu_list(list_dict):
            item['depth'] = current_depth
            item['url'] = self.get_url(item)
            item['selected'] = self.is_selected(item)
            item['submenu'] = self.get_submenu_list(item, depth=current_depth + 1)
            visible_menu.append(item)

        self.process_breadcrums(visible_menu)

        return visible_menu


class Menu(MenuBase):
    """
    Class that generates menu list.
    """
    def __call__(self, request, list_dict):
        self.save_user_state(request)
        return self.generate_menu(list_dict)

generate_menu = Menu()
