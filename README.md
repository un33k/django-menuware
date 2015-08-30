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


How to use
====================
Let's add a left / right navigation to an application called `foobar`.

    Directory structure:
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
