from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'status']

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']
        read_only_fields = ['status','created_at', 'updated_at']

    def validate_status(self, value):
        if value not in [Task.TaskStatus.COMPLETED]:
            raise serializers.ValidationError("Only 'completed' status can be set using this endpoint.")
        return value