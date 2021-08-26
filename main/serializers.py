from main.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


def in_three_days():
    return timezone.now() + datetime.timedelta(days=3)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class TaskListSerializer(serializers.ModelSerializer):
    time_left = serializers.SerializerMethodField()

    def get_time_left(self, obj):
        if obj.date_finished_planned:
            return obj.date_finished_planned-obj.date_created

    class Meta:
        model = Task
        fields = '__all__'


class TaskStatusChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskStatusChange
        optional_fields = ['task', 'prev_status', 'user']
        fields = '__all__'


class ReminderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reminder
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
