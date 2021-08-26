
from django.db import models
from django.db.models import Q


class TaskChangeManager(models.Manager):
    # if i changed any task status or someone changed to my task
    def get_my_changes(self, user):
        queryset = self.select_related('task', 'task__performer', 'user').filter(
            Q(user=user) | Q(task__performer=user))
        return queryset


class TaskManager(models.Manager):
    # if i changed any task status or someone changed to my task
    def get_my_tasks(self, user_id):
        queryset = self.filter(performer_id=user_id)
        return queryset

    def get_my_tasks_observe(self, user_id):
        queryset = self.prefetch_related(
            'observers').filter(observers__id=user_id, many=True)
        return queryset
