
from django.db import models
from django.db.models import Q


class TaskChangeManager(models.Manager):
    # if i changed any task status or someone changed to my task
    def get_my_changes(self, queryset, user):
        queryset = queryset.select_related('task', 'task__performer', 'user').filter(
            Q(user=user) | Q(task__performer=user))
        return queryset
