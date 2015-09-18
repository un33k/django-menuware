DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
SECRET_KEY = "un33k"
INSTALLED_APPS = ['menuware']
MIDDLEWARE_CLASSES = []
ROOT_URLCONF = 'menuware.tests.urls'

MENUWARE_SUBMENU = [
    {
        "name": "submenu",
        "url": '/submenu/',
        "render_for_authenticated": True,
    },
]

MENUWARE_MENU = [
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
        "submenu": MENUWARE_SUBMENU,
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
