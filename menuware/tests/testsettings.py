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

NAV_MENU = [
    {
        "name": "Main",
        "url": "/",
    },
    {
        "name": "Account",
        "url": "/account",
        "validators": ["menuware.utils.is_authenticated", ],
        "submenu": [
            {
                "name": "Profile",
                "url": '/account/profile/',
            },
        ],
    },
]
