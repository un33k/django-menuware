from django.conf import settings

MENU_NOT_FOUND = [
    {
        "name": "MENU NOT FOUND",
        "url": "/",
        "render_for_unauthenticated": True,
        "render_for_authenticated": True,
    },
]

MENUWARE_MENU = getattr(settings, 'MENUWARE_MENU', {})
