from django.core.mail import EmailMultiAlternatives
from telegram import Bot

from celery import shared_task

from autoweb.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


bot = Bot(token=TELEGRAM_TOKEN)


@shared_task()
def send_telegram_message(message):
    bot.send_message(
        chat_id=TELEGRAM_CHAT_ID, text=message
    )


@shared_task()
def send_email_task(
    subject, plain_message, from_email, to_email, html_message
):
    email = EmailMultiAlternatives(
        subject, plain_message, from_email, to_email
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()
