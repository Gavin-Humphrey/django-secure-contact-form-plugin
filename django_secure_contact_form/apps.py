from django.apps import AppConfig


class DjangoSecureContactFormConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_secure_contact_form"


class DjangoSecureContactFormConfig(AppConfig):
    name = 'django_secure_contact_form'

    def ready(self):
        import django_secure_contact_form.signals