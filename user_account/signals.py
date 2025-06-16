from asgiref.sync import async_to_sync
from channels.layers import channel_layers, get_channel_layer
from django.db import models
from django.dispatch import receiver
from notification.models import Notification
from user_account.models import User, RatingandReview
import os
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(models.signals.post_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    try:
        old_image = User.objects.get(pk=instance.pk).profile_picture
    except User.DoesNotExist:
        return False
    
    new_image = instance.profile_picture

    if bool(old_image) and new_image != old_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(models.signals.m2m_changed, sender=User.followers.through)
def follow_notification(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        for follower_id in pk_set:
            follower = User.objects.get(id=follower_id)
            Notification.objects.create(
                user=instance,
                message=f"\"{follower.username}\" started following you.",
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{instance.id}",
                {
                    "type": "send_notification",
                    "notification": {
                        "message": f"\"{follower.username}\" started following you.",
                    }
                }
            )


@receiver(models.signals.post_save, sender=RatingandReview)
def create_review_notification(sender, instance, created, **kwargs):

    Notification.objects.create(
        user=instance.user,
        message= f"You’ve got a new rating & review from \"{instance.reviewer.username}\".",
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{instance.user.id}",
        {
            "type": "send_notification",
            "notification": {
                
                "message": f"You’ve got a new rating & review from \"{instance.reviewer.username}\".",
            }
        }
    )

