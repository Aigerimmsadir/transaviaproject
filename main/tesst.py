from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask,PeriodicTasks, IntervalSchedule
import json
from main.models import *
from datetime import datetime,timedelta

from django.contrib.auth.models import User
PeriodicTask.objects.all().delete()
# t = Task(performer_id=1, name='hh')
# print('kk')
# t.save()
# # t.date_finished_planned=date_finished_planned
# t.save()
# print(Reminder.objects.all())
# celery -A transavia beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# python3 manage.py shell
# python3 manage.py runserver
# exec(open('/workspace/main/tesst.py').read())
# celery -A transavia worker -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# from celery import current_app 
# tasks = current_app.tasks.keys()
# print(tasks)
