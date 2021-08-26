from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action  # list_route, detail_route
from rest_framework.response import Response
from main.models import *
from main.serializers import *
from rest_framework import permissions
from django.utils import timezone


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().prefetch_related(
        'observers').select_related('performer')
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            serializer_class = TaskSerializer
        else:
            serializer_class = TaskListSerializer
        return serializer_class

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk):
        new_status = request.data.get('new_status')
        task = self.get_object()
        prev_status = task.status
        # not very pretty solution but it handles errors
        task_change_data = {
            "prev_status": prev_status,
            "new_status": new_status,
            "task": task.id,
            "user": request.user.id
        }
        task_status_change_serializer = TaskStatusChangeSerializer(
            data=task_change_data)
        if task_status_change_serializer.is_valid():

            task_status_change_serializer.save()
            task.status = new_status
            if new_status == Task.COMPLETED:
                task.date_finished = timezone.now()
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=200)
        return Response({'error': "not valid input data"}, status=400)
    
    @action(detail=False, methods=['get'])
    def get_my_tasks(self, request):
        only_mine=request.data.get('only_mine', True)
        user_id=request.user.id
        if only_mine:
            queryset=Task.objects.get_my_tasks(user_id)
        else:
            queryset=Task.objects.get_my_tasks_observe(user_id)
        data=self.serializer_class(queryset,many=True).data
        return Response(data, status=200)
    


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TaskStatusChangeViewSet(viewsets.ModelViewSet):
    queryset = TaskStatusChange.objects.select_related('user', 'task').all()
    serializer_class = TaskStatusChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #
    @action(detail=False, methods=['get'])
    def my_changes(self, request):
        # using manager we get all my changes or changes to my tasks
        queryset = TaskStatusChange.objects.get_my_changes(
            request.user)
        changes = TaskStatusChangeSerializer(queryset, many=True)
        return Response(changes.data, status=200)


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.prefetch_related('users').all()
    serializer_class = ReminderSerializer
    permission_classes = (permissions.IsAuthenticated,)
