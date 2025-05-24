from django.apps import AppConfig
from django.conf import settings
import threading

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .tasks import import_random_users

        def start_import():
            count = 1000
            chunk = settings.CHUNK_SIZE
            while count > 0:
                request_cnt = min(count, chunk)
                import_random_users.delay(request_cnt)
                count -= request_cnt

        threading.Thread(target=start_import).start()