from django.apps import AppConfig


class PUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'p_users'

    def ready(self):
        import p_users.signals
