from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Advertisement
from .tasks import send_notification

@receiver(post_save, sender=Advertisement)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        send_notification.delay(instance.id)