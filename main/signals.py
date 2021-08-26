from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from main.models import *
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from main.tasks import *
import json


@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    # if no reminder yet then start waiting for due date
    if not Reminder.objects.filter(task=instance.id).exists():
        # every day
        schedule, newsch = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.SECONDS,
        )
        executor = instance.performer.id
        observers = [int(o.id)for o in instance.observers.all()]
        observers.append(executor)
        task_name = 'Sending mail{}'.format(instance.id)
        # periodic task that will send emails everyday
        PeriodicTask.objects.create(
            interval=schedule,
            name=task_name,
            task='send_mail_custom',
            args=json.dumps(
                [observers, instance.date_finished_planned.isoformat(), instance.id])

        )
    if instance.status == Task.COMPLETED:
        # if task is completed then no need to send messages anymore
        PeriodicTask.objects.get(
            name='Sending mail{}'.format(instance.id)).delete()
