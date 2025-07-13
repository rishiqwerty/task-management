from rest_framework import viewsets, status, throttling
from rest_framework.decorators import action, parser_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, TextToTaskSerializer

class LLMApiThrottle(throttling.AnonRateThrottle):
    rate = '20/minute'

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def get_throttles(self):
        # Apply throttle to create, update, and text_to_task_action
        if self.action in [
            'create', 'update', 'partial_update', 'text_to_task_action'
        ]:
            return [LLMApiThrottle()]
        return super().get_throttles()

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    @parser_classes([])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status == Task.TaskStatus.COMPLETED:
            return Response({"detail": "Task is already completed."}, status=status.HTTP_400_BAD_REQUEST)

        task.status = Task.TaskStatus.COMPLETED
        task.completed_at = timezone.now()
        task.save()

        return Response({"detail": "Task marked as completed."}, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['post'], 
        serializer_class=TextToTaskSerializer
    )
    def text_to_task_action(self, request):
        """Process a text prompt to create or update a task.
        This will create multiple tasks based on the text prompt.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result=serializer.save()

        return Response({"detail": result}, status=status.HTTP_200_OK)

