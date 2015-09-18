from django import template
from django.conf import settings

from ..menu import generate_menu
from .. import defaults as defs

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu(context, name):
    """
    Returns a consumable menu list for a given menu name, if the name is found in the
    `MENUWARE_MENU` field of settings.py, or it returns an empty list.
    """
    menu_list = defs.MENUWARE_MENU.get(name, getattr(settings, name, defs.MENU_NOT_FOUND))
    return generate_menu(context['request'], menu_list)
