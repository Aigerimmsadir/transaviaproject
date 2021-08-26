from celery import shared_task
from main.models import *
import datetime
from django.core.mail import send_mail
from django.utils import timezone
from transavia.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User


@shared_task(name="send_mail_custom")
def send_mail_custom(users_list, date_finished_planned, task_id):
    # check if it is less than 3 days until planned due date
    print(date_finished_planned)

    date_finished_planned = datetime.datetime.fromisoformat(
        date_finished_planned)
    if date_finished_planned and timezone.now()-date_finished_planned <= datetime.timedelta(days=3):
        r = Reminder(task_id=task_id, text='dd')
        r.save()
        emails_send = []
        for u in users_list:
            r.users.add(u)
            user = User.objects.get(id=u)
            emails_send.append(user.email)
        # so if its less than 3 days it will send emails every day
        send_mail(
            'Do not remember to finish task Sending mail{}'.format(task_id),
            'Here is the message.',
            EMAIL_HOST_USER,
            emails_send,
            fail_silently=False,
        )
