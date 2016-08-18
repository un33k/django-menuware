from django import template
from django.conf import settings

from ..menu import generate_menu
from .. import defaults as defs

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu(context, menu_name):
    """
    Returns a consumable menu list for a given menu_name found in settings.py.
    Else it returns an empty list.
    """
    menu_list = getattr(settings, menu_name, defs.MENU_NOT_FOUND)
    return generate_menu(context['request'], menu_list)
