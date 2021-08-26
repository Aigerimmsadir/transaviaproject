from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime,timedelta
from django.utils import timezone
from main.managers import *

def return_date_time():
    now = timezone.now()
    return now + timedelta(days=7)


class Task(models.Model):
    TO_DO=0
    ACTIVE=1
    CONTROL=2
    COMPLETED=3
    STATES = (
        (0, 'TO_DO'),
        (1, 'ACTIVE'),
        (2, 'CONTROL'),
        (3, 'COMPLETED')
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000,blank=True, null=True)
    performer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='tasks', null=True)
    observers = models.ManyToManyField(User, related_name='observing_tasks',
                                       db_index=True)
    status = models.PositiveSmallIntegerField(default=0, choices=STATES)
    date_created = models.DateTimeField(default=timezone.now)
    date_finished = models.DateTimeField(null=True)
    # automatically is in 7 days after the start
    date_finished_planned = models.DateTimeField(default=return_date_time)


class TaskStatusChange(models.Model):
    TO_DO=0
    ACTIVE=1
    CONTROL=2
    COMPLETED=3
    STATES = (
        (TO_DO, 'TO_DO'),
        (ACTIVE, 'ACTIVE'),
        (CONTROL, 'CONTROL'),
        (COMPLETED, 'COMPLETED')
    )
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, related_name='status_changes')
    prev_status = models.PositiveSmallIntegerField(choices=STATES)
    new_status = models.PositiveSmallIntegerField(choices=STATES)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='tasks_changed_status', null=True)
    objects = TaskChangeManager()


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1000)
    users = models.ManyToManyField(User, related_name='reminders',
                                   db_index=True)
