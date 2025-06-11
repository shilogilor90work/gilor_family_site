from django.apps import AppConfig


class FinanceTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance_tracker'

    def ready(self):
        import finance_tracker.signals # Import signals here