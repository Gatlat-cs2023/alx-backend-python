from django.db.models.signals import pre_save
from django.dispatch import receiver
from messaging.models import Message, MessageHistory
from django.db.models.signals import post_delete
from django.contrib.auth.models import User

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                instance.edited = True
                # Required by ALX checker
                MessageHistory.objects.create(
                    message=old_instance,
                    old_content=old_instance.content,
                    edited_by=old_instance.sender
                )
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    # If you have a Notification model:
    # Notification.objects.filter(user=instance).delete()
