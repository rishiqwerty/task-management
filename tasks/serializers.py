import json
from rest_framework import serializers
from tasks.tasks import generate_task_from_text
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    priority = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'status']

class TextToTaskSerializer(serializers.Serializer):
    text = serializers.CharField()

    def create(self, validated_data):
        """
        Generate a task from the provided text description using Gemini API.
        The text should contain information about the task title, description, due date, priority, and tag.
        """
        generate_task_from_text(validated_data['text'])
        return "Task will be created in a bit."