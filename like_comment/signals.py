from django.db import models
from .models import Like, Comment, CommentReply
from notification.models import Notification
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(models.signals.post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        if instance.user == instance.post.user:
            return
        
        Notification.objects.create(
            user=instance.post.user,
            message=f"\"{instance.user.username}\" liked your post \"{instance.post.title}\".",
        )
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.post.user.id}",
            {
                "type": "send_notification",
                "notification": {
                    "post": instance.post.id,
                    "message": f"\"{instance.user.username}\" liked your post \"{instance.post.title}\".",
                }
            }
        )


@receiver(models.signals.post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        if instance.user == instance.post.user:
            return
        
        Notification.objects.create(
            user=instance.post.user,
            post=instance.post,
            message=f"\"{instance.user.username}\" commented on your post \"{instance.post.title}\".",
        )
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.post.user.id}",
            {
                "type": "send_notification",
                "notification": {
                    "post": instance.post.id,
                    "message": f"\"{instance.user.username}\" commented on your post \"{instance.post.title}\".",
                }
            }
        )


@receiver(models.signals.post_save, sender=CommentReply)
def create_comment_reply_notification(sender, instance, created, **kwargs):
    if created:
        target_user = instance.comment.user if instance.comment else instance.parent.user
        
        if instance.user == target_user:
            return
        
        Notification.objects.create(
            user=target_user,
            post=instance.post,
            message=f"\"{instance.user.username}\" replied to your comment on post \"{instance.post.title}\".",
        )
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{target_user.id}",
            {
                "type": "send_notification",
                "notification": {
                    "post": instance.post.id,
                    "message": f"\"{instance.user.username}\" replied to your comment on post \"{instance.post.title}\".",
                }
            }
        )


