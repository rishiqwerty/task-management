from django.db import models
from django.utils import timezone

class Task(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        OVERDUE = 'overdue', 'Overdue'
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default='pending'
    )
    due_date = models.DateTimeField()
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