from django.apps import AppConfig


class MenuAppConfig(AppConfig):
    name = 'menuware'
    label = 'menuware'
    verbose_name = 'Menu Application'

    def ready(self):
        pass
