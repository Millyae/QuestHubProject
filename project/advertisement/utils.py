import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_token(length=64):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def send_verification_email(user, token):
    subject = 'Verify Your Email Address'
    html_message = render_to_string('email/verification_email.html', {
        'user': user,
        'token': token,
    })
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'from@example.com', [user.email], html_message=html_message)
