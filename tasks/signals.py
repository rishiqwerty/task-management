from tasks.models import Task
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from tasks.tasks import assign_task_priority
from django.db import transaction

@receiver(pre_save, sender=Task)
def task_pre_save(sender, instance, **kwargs):
    # Automatically update status based on due date and current time
    old_priority = Task.objects.filter(id=instance.id).values_list('priority', 'tag').first() if instance.id else None
    print(instance.priority, instance.tag)
    if old_priority and not instance.priority:
        print("Pre-save signal triggered for Task instance.")
        if old_priority[0] != instance.priority:
            transaction.on_commit(lambda: assign_task_priority.delay(instance.id))
    
    if old_priority and not instance.tag:
        instance.tag = old_priority[1]
            
    

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        if not instance.priority:
            transaction.on_commit(lambda: assign_task_priority.delay(instance.id))
        print(f"New task created: {instance.title} (ID: {instance.id})")
