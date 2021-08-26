from celery import shared_task
from main.models import *
import datetime
from django.core.mail import send_mail
from django.utils import timezone
from transavia.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User

from django_celery_beat.models import PeriodicTask


@shared_task(name="send_mail_custom")
def send_mail_custom(users_list, date_finished_planned, task_id):
    # check if it is less than 3 days until planned due date
    print(date_finished_planned)

    date_finished_planned = datetime.datetime.fromisoformat(
        date_finished_planned)
    email_text = ''
    now_time = timezone.now()
    # if less than 3 days left to due date start sending emails
    if date_finished_planned and now_time-date_finished_planned <= datetime.timedelta(days=3):
        email_text = 'Do not remember to finish task Sending mail{}'.format(
            task_id)
        # if you have already missed due date, then stop sending reminders
        if date_finished_planned<timezone.now():
            email_text = 'You have forgotten to finish task Sending mail{}'.format(
                task_id)
            PeriodicTask.objects.filter(
                name='Sending mail{}'.format(task_id)).delete()
            print('deleted')

        r = Reminder(task_id=task_id, text=email_text)
        r.save()
        emails_send = []
        for u in users_list:
            r.users.add(u)
            user = User.objects.get(id=u)
            emails_send.append(user.email)
        # so if its less than 3 days it will send emails every day
        send_mail(
            email_text,
            'Here is the message.',
            EMAIL_HOST_USER,
            emails_send,
            fail_silently=False,
        )
