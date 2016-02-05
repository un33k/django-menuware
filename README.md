Django Menuware
====================

**A simple yet effective menu generator for any Django project**

[![status-image]][status-link]
[![version-image]][version-link]
[![coverage-image]][coverage-link]
[![download-image]][download-link]


Overview
====================

Build **simple navigation system** for Django projects/apps, while keeping it **DRY**.

How to install
====================

    1. easy_install django-menuware
    2. pip install django-menuware
    3. git clone http://github.com/un33k/django-menuware
        a. cd django-menuware
        b. run python setup.py
    4. wget https://github.com/un33k/django-menuware/zipball/master
        a. unzip the downloaded file
        b. cd into django-menuware-* directory
        c. run python setup.py

How to use (Simple)
====================
Once you have installed `django-menuware`, then add `menuware` to your INSTALLED_APPS.

   ```python
    # Add `MENUWARE_MENU` to your settings.py and set it up as per your requirements.
    ####################################################################################
    # The following example should help you with the layout.
    # Please note:
    #   "url" can be hard-coded or `reversible`. (e.g. '/foo/bar/' vs. 'foo_url_view').
    #   Minimally set one of `"render_for_unauthenticated" or "render_for_authenticated"`.
    #   Sub-menu items inherit the `render` attributes of their parent menu item.
    #   Menu items get a `selected` attribute indicating their `active` state.
    #   It first looks inside MENUWARE_MENU to load the menu list, if not found, then it looks
    #   at the settings directly. (e.g. {% get_menu "ACCOUNT_MENU" as account_menu %} )
    ####################################################################################

    ACCOUNT_MENU = [
        {
            "name": "Profile",
            "url": "/account/profile/",
            "render_for_authenticated": True,
        },
        {
            "name": "Preferences",
            "url": "/account/preferences/",
            "render_for_authenticated": True,
        },
        {
            "name": "Social Links",
            "url": "/account/social/",
            "render_for_authenticated": True,
        }
    ]

    MENUWARE_MENU = {
        "RIGHT_NAV_MENU": [
            {   # Show `Login` to `unauthenticated` users ONLY
                "name": "Login",
                "url": "/login/",
                "render_for_unauthenticated": True,
            },
            {   # Show `Account` to `authenticated` users ONLY
                "name": "Account",
                "url": "/account/",
                "render_for_authenticated": True,
                "submenu": ACCOUNT_MENU,
            },
            {   # Show `Logout` to `authenticated` users ONLY
                "name": "Logout",
                "url": "/logout/",
                "render_for_authenticated": True,
            },
        ],
        "LEFT_NAV_MENU": [
            {   # Show `Home` to all users
                "name": "Home",
                "url": "/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Show `Search` to all users
                "name": "Search",
                "url": "/search/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Show `Comment Admin` to `staff` users ONLY
                "name": "Comment Admin",
                "url": "/review/admin/",
                "render_for_authenticated": True,
                "render_for_staff": True,
            },
            {   # Show `Admin` to `superuser` ONLY
                "name": "Admin",
                "url": "admin:index", # Reversible
                "render_for_authenticated": True,
                "render_for_superuser": True,
                "submenu": [  # Show submenu to those who could see the `parent` menu
                    {
                        "name": "Switch", # switch to user account (su)
                        "url": "/account/profile/switch",
                    },
                ],
            },
        ],
        "LEFT_FOOTER_MENU": [
            {
                "name": "Contact Us",
                "url": "/contact/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
        ],
        "RIGHT_FOOTER_MENU": [
            {
                "name": "Terms and Conditions",
                "url": "/terms-condition/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # `portal.utils` will be imported and `is_not_main_site(request)` will be called (dotted notations only)
                "name": "Blog",
                "url": "/blog",
                "render_for_unauthenticated": True,
                "render_for_user_when_condition_is_true": "portal.utils.is_not_main_site",
            },
            {   # `portal.utils` will be imported and `is_user_is_paid_customer(request)` will be called (dotted notations only)
                "name": "Blog",
                "url": "/blog",
                "render_for_authenticated": True, # login is required to check if user is a paid customer
                "render_for_user_when_condition_is_true": "portal.utils.is_user_is_paid_customer",
            },
            {   # `portal.utils` will be imported and `is_user_is_paid_customer(request)` will be called (dotted notations only)
                "name": "Upgrade",
                "url": "/upgrade",
                "render_for_authenticated": True, # if free-tier user, promote upgrade
                "render_for_user_when_condition_is_false": "portal.utils.is_user_is_paid_customer",
            },
        ]
    }
   ```
In your template, load the templatetags for building your menu.

   ```html
    <!-- base.html -->
    {% load menuware %}

    <!DOCTYPE html>
    <html>
        <head><title>Django Menuware</title></head>
        <body>
            <!-- NAV BAR Start -->
            {% get_menu "LEFT_NAV_MENU" as left_menu %}
            <div style="float:left;">
                {% for item in left_menu %}
                    <li class="{% if item.selected %} active {% endif %}">
                        <a href="{{item.url}}">{{item.name}}</a>
                    </li>
                    {% if item.submenu %}
                        <ul>
                        {% for menu in item.submenu %}
                            <li class="{% if menu.selected %} active {% endif %}">
                                <a href="{{menu.url}}">{{menu.name}}</a>
                            </li>
                        {% endfor %}
                        </ul>
                    {% endif %}
                {% endfor %}
            </div>

            {% get_menu "RIGHT_NAV_MENU" as right_menu %}
            <div style="float:right;">
                {% for item in right_menu %}
                    <li class="{% if item.selected %} active {% endif %}">
                        <a href="{{item.url}}">{{item.name}}</a>
                    </li>
                    {% if item.submenu %}
                        <ul>
                        {% for menu in item.submenu %}
                            <li class="{% if menu.selected %} active {% endif %}">
                                <a href="{{menu.url}}">{{menu.name}}</a>
                            </li>
                        {% endfor %}
                        </ul>
                    {% endif %}
                {% endfor %}
            </div>
            <!-- NAV BAR End -->

            <!-- Footer Start -->
            {% get_menu "LEFT_FOOTER_MENU" as left_footer_menu %}
            <div style="float:left;">
                <!-- loop through your left footer menus -->
            </div>

            {% get_menu "RIGH_FOOTER_MENU" as right_footer_menu %}
            <div style="float:right;">
                <!-- loop through your right footer menus -->
            </div>
            <!-- Footer End -->
        </body>
    </html>
   ```

How to use (Advanced)
====================
Let's add a left / right navigation to an application called `foobar`.


    Install `django-menuware`.
    Note: you don't need to add `menuware` to your INSTALLED_APPS in this example.

    Directory structure:
    ####################
    foobar/__init__.py
    ... other app related dirs / files
    foobar/templatetags
    foobar/templatetags/__init__.py
    foobar/templatetags/foobar_menu.py
    foobar/templates/partial_header_left_menu.html
    foobar/templates/partial_header_right_menu.html
    foobar/templates/header_menu.html

   ```python
    # in foobar/templatetags/foobar_menu.py
    from django import template
    from menuware.menu import generate_menu
    register = template.Library()

    # custom template tag to render the right navigation menu
    @register.assignment_tag(takes_context=True)
    def foobar_header_menu_right(context):
        """
        Returns a navigation menu for the top-right header
        """
        RIGHT_NAV_MENU = [
            {   #  Show `Login` to `unauthenticated` users ONLY
                "name": "Login",
                "url": "/login/",
                "render_for_unauthenticated": True,
            },
            {   #  Show `Logout` to `authenticated` users ONLY
                "name": "Logout",
                "url": "/logout/",
                "render_for_authenticated": True,
            },
        ]
        return generate_menu(context['request'], RIGHT_NAV_MENU)

    # custom template tag to render the left navigation menu
    @register.assignment_tag(takes_context=True)
    def foobar_header_menu_left(context):
        """
        Returns a navigation menu for the top-left header
        """
        LEFT_NAV_MENU = [
            {   # Show `Home` to all users
                "name": "Home",
                "url": "/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Show `Search` to all users
                "name": "Search",
                "url": "/search/",
                "render_for_unauthenticated": True,
                "render_for_authenticated": True,
            },
            {   # Show `Comment Admin` to `staff` users ONLY
                "name": "Comment Admin",
                "url": "/review/admin/",
                "render_for_authenticated": True,
                "render_for_staff": True,
            },
            {   # Show `Account Admin` to `superuser` ONLY
                "name": "Account Admin",
                "url": "/account/admin/",
                "render_for_authenticated": True,
                "render_for_superuser": True,
            },
        ]
        return generate_menu(context['request'], LEFT_NAV_MENU)
   ```

   ```html
    # foobar/templates/partial_header_right_menu.html
    {% load foobar_menu %}
    {% foobar_header_menu_right as menu %}

    {% for item in menu %}
        <li class="{% if item.selected %} active {% endif %}">
            <a href="{{item.url}}">{{item.name}}</a>
        </li>
    {% endfor %}
   ```

   ```html
    # foobar/templates/partial_header_left_menu.html
    {% load foobar_menu %}
    {% foobar_header_menu_left as menu %}

    {% for item in menu %}
        <li class="{% if item.selected %} active {% endif %}">
            <a href="{{item.url}}">{{item.name}}</a>
        </li>
    {% endfor %}
   ```

   ```html
    # foobar/templates/header_menu.html
    <!DOCTYPE html>
    <html>
        <head><title>Django Menuware</title></head>
        <body>
            <div style="float:left;">
                {% include "foobar/partial_header_left_menu.html" %}
            </div>

            <div style="float:right;">
                {% include "foobar/partial_header_right_menu.html" %}
            </div>
        </body>
    </html>
   ```

Running the tests
====================

To run the tests against the current environment:

    python manage.py test


License
====================

Released under a ([BSD](LICENSE.md)) license.


Version
====================
X.Y.Z Version

    `MAJOR` version -- when you make incompatible API changes,
    `MINOR` version -- when you add functionality in a backwards-compatible manner, and
    `PATCH` version -- when you make backwards-compatible bug fixes.

[status-image]: https://secure.travis-ci.org/un33k/django-menuware.png?branch=master
[status-link]: http://travis-ci.org/un33k/django-menuware?branch=master

[version-image]: https://img.shields.io/pypi/v/django-menuware.svg
[version-link]: https://pypi.python.org/pypi/django-menuware

[coverage-image]: https://coveralls.io/repos/un33k/django-menuware/badge.svg
[coverage-link]: https://coveralls.io/r/un33k/django-menuware

[download-image]: https://img.shields.io/pypi/dm/django-menuware.svg
[download-link]: https://pypi.python.org/pypi/django-menuware
