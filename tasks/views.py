from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == 'complete':
            return TaskStatusUpdateSerializer
        return TaskSerializer

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    @parser_classes([])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status == Task.TaskStatus.COMPLETED:
            return Response({"detail": "Task is already completed."}, status=status.HTTP_400_BAD_REQUEST)

        task.status = Task.TaskStatus.COMPLETED
        task.save()

        return Response({"detail": "Task marked as completed."}, status=status.HTTP_200_OK)

# Validate due date is in the future