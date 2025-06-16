from django.apps import AppConfig


class LikeCommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'like_comment'

    def ready(self):
        from .import signals
        return super().ready()
