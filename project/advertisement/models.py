# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Advertisement(models.Model):
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DPS', 'ДД'),
        ('Traders', 'Торговцы'),
        ('GuildMasters', 'Гилдмастеры'),
        ('QuestGivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Alchemists', 'Зельевары'),
        ('SpellMasters', 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to', blank=True)
    images = models.ManyToManyField('AdvertisementImage', related_name='advertisements', blank=True)
    video_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('advertisement_detail', args=[str(self.id)])

    def notify_responses(self):
        for response in self.responses.all():
            subject = f"Новый отклик на ваше объявление '{self.title}'"
            message = render_to_string('email/response_notification.html', {'response': response})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'your_email@example.com', [response.author.email], html_message=message)

class AdvertisementImage(models.Model):
    image = models.ImageField(upload_to='advertisement_images/')

    def __str__(self):
        return f"Image{self.id}"

class Response(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='responses', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response by {self.author} on {self.advertisement.title}"

@receiver(post_save, sender=Advertisement)
def notify_author_on_response(sender, instance, created, **kwargs):
    if created and instance.responses.exists():
        instance.notify_responses()

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.token}'
