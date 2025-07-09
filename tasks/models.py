from datetime import datetime
from django.db import models
from django.utils import timezone

class Task(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        OVERDUE = 'overdue', 'Overdue'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default='pending'
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        null=True,
        blank=True,
    )
    tag = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'work', 'personal',
    notes = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField()
    create_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically update status based on due date and current time
        # IF the task is not completed and has a due date
        # If the due date is in the past, set status to OVERDUE
        # If the status is not IN_PROGRESS, CANCELLED, or COMPLETED, set status
        if self.status != 'completed' and self.due_date:
            if self.due_date < timezone.now():
                self.status = self.TaskStatus.OVERDUE
            elif self.status not in [self.TaskStatus.IN_PROGRESS, self.TaskStatus.CANCELLED, self.TaskStatus.COMPLETED]:
                self.status = self.TaskStatus.PENDING
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class PromptResponse(models.Model):
    text = models.TextField()
    prompt_response = models.TextField(blank=True, null=True)
    status = models.JSONField(default=dict)  # Store status of task creation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PromptResponse: {self.text[:50]}..."  # Display first 50 characters
