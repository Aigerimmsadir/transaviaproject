
from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt import views as jwt_views
from django.contrib import admin
from .views import *

router = routers.DefaultRouter()  # trailing_slash=False
router.register(r'task', TaskViewSet, basename='task')
router.register(r'user', UserViewSet, basename='user')
router.register(r'task_status_change', TaskStatusChangeViewSet, basename='task_status_change')
router.register(r'reminder', ReminderViewSet, basename='reminder')


urlpatterns = [
    path('', include(router.urls)),
]


