from celery import shared_task
from django.core.mail import send_mail
from .models import Advertisement

@shared_task
def send_notification(ad_id):
    ad = Advertisement.objects.get(id=ad_id)
    subscribers = ad.subscribers.all()
    recipients = [subscriber.email for subscriber in subscribers]
    subject = "Новое объявление на доске"
    message = f"Новое объявление: {ad.title}\nПрочитать: {ad.get_absolute_url()}"
    send_mail(subject, message, 'from@example.com', recipients)

@shared_task
def send_weekly_newsletter():
    latest_ads = Advertisement.objects.order_by('-created_at')[:5]
    recipients = set(sub.email for ad in latest_ads for sub in ad.subscribers.all())
    subject = "Еженедельная рассылка объявлений"
    message = "Последние объявления:\n"
    for ad in latest_ads:
        message += f"- {ad.title}: {ad.get_absolute_url()}\n"
    send_mail(subject, message, 'from@example.com', recipients)