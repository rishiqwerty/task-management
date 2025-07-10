from datetime import datetime, timedelta
import json
from celery import shared_task
from django.utils import timezone
from datetime import timezone as dt_timezone
from .models import Task, PromptResponse
from tasks.prompt import VALID_PRIORITIES, generate_task_from_text_prompt, generate_task_prioritization_prompt, gemini_api_call, openai_api_call

@shared_task
def mark_overdue_tasks():
    """Mark tasks as overdue if they are pending or in progress and past their due date."""
    overdue_count = Task.objects.filter(
        status__in=[Task.TaskStatus.PENDING, Task.TaskStatus.IN_PROGRESS],
        due_date__lt=timezone.now()
    ).update(status=Task.TaskStatus.OVERDUE)
    return f"{overdue_count} tasks marked as overdue."

@shared_task
def reprioritize_tasks():
    """
    Reprioritize tasks based on urgency and importance using Gemini API.
    This task fetches tasks that are pending or in progress and due within the next 7 days,
    generates a prompt for the Gemini API, and updates their priorities based on the response.
    """
    try:
        relevant_tasks = Task.objects.filter(
            status__in=[Task.TaskStatus.PENDING, Task.TaskStatus.IN_PROGRESS],
            due_date__lte=timezone.now() + timedelta(days=7)
        ).order_by('due_date')[:50]
        prompt = generate_task_prioritization_prompt(relevant_tasks)
        predictions = openai_api_call(prompt)
        # predictions = gemini_api_call(prompt)
        p=PromptResponse.objects.create(
            text=prompt,
            prompt_response=predictions
        )
        try:
            predictions = json.loads(predictions)
        except json.JSONDecodeError:
            predictions = predictions.strip().splitlines()[1]
            predictions = json.loads(predictions)

        for task_id, prediction in predictions.items():
            priority = prediction.get('priority', Task.Priority.MEDIUM)
            tag = prediction.get('tag', 'general')
            if priority not in VALID_PRIORITIES:
                priority = Task.Priority.MEDIUM  # default fallback
            t=Task.objects.get(id=task_id)
            t.priority = priority
            t.tag = tag
            t.save()
        p.status = {
            'status': 'success',
            'message': f"Reprioritized {len(predictions)} tasks successfully."
        }
        p.save()
    except Exception as e:
        p.status = {
            'status': 'error',
            'message': f"Error reprioritizing tasks: {str(e)}"
        }
        p.save()
        print(f"Error reprioritizing tasks: {e}")


@shared_task
def assign_task_priority(task_id):
    """Assign priority to a task based on its urgency and importance using Gemini API."""
    try:
        current_task = Task.objects.filter(id=task_id).values_list(
            'id', 'title', 'due_date', 'description', 'priority', 'tag'
        ).first()
        task = Task.objects.filter(due_date__gte=current_task[2], status__in=[Task.TaskStatus.PENDING]).values_list(
            'id', 'title', 'due_date', 'description', 'priority', 'tag'
        ).order_by('-due_date')[:10]
        prompt = f"""You are a task prioritization assistant.
                    Here are 10 existing tasks and a new task.
                    Older tasks: {task}
                    New task: {current_task}
                    Based on the urgency and importance of these tasks, please
                    assign a priority as one of these values only: {', '.join(VALID_PRIORITIES)}.
                    And tag them with kind of task they are, like 'work', 'personal', 'urgent', etc.
                    Respond with a single word for priority — one of: {', '.join(VALID_PRIORITIES)}.
                    And a tag for each task, like 'work', 'personal', 'urgent', etc.
                    Return a JSON mapping task id to their priority and tag only for this new task.
                    Respond with a raw JSON object like an api response:
                    Important: Return a valid JSON object. 
                    Keys must be enclosed in double quotes. 
                    Values must be enclosed in double quotes (if strings) or valid JSON numbers. 
                    Do not add extra spaces or new lines in the JSON object.
                    Do not wrap your response in code block markers.
                    """+ '{1: {"priority":"pending", "tag": "Work"}'
        # predictions = gemini_api_call(prompt).strip().splitlines()[1]
        response = openai_api_call(prompt)
        p = PromptResponse.objects.create(
            text=prompt,
            prompt_response=response
        )
        status = {'task': "Creating task from text", 'status': 'in_progress'}
        try:
            predictions = json.loads(response)
        except json.JSONDecodeError:
            predictions = response.strip().splitlines()[1]
            predictions = json.loads(predictions)
        for task_id, prediction in predictions.items():
            priority = prediction.get('priority', Task.Priority.MEDIUM)
            tag = prediction.get('tag', 'general')
            if priority not in VALID_PRIORITIES:
                priority = Task.Priority.MEDIUM  # default fallback
            t=Task.objects.get(id=int(task_id))
            t.priority = priority
            t.tag = tag
            t.save()
        status['status'] = {
            'status': 'success',
            'message': f"Reprioritized tasks successfully."
        }
        p.save()
        print(f"Task ID {task_id} priority assigned successfully: {priority}, tag: {tag}")
    except Exception as e:
        status['error'] = str(e)
        print(f"Error assigning priority for task ID {task_id}: {e}")
    finally:
        p.status = status
        p.save()

@shared_task
def generate_task_from_text(text):
    """
    Generate a task from a text description using Gemini API.
    The text should contain information about the task title, description, due date, priority, and tag.
    """
    prompt = generate_task_from_text_prompt(text)
    response = openai_api_call(prompt)
    # response = gemini_api_call(prompt)
    p = PromptResponse.objects.create(
        text=prompt,
        prompt_response=response
    )
    status = {
        'task': "Creating task from text",
        'status': "in_progress"
    }
    try:
        try:
            task_data = json.loads(response)
        except json.JSONDecodeError:
            response = response.strip().splitlines()[1]
            task_data = json.loads(response)
        for task in task_data:
            due_date = datetime.strptime(task.get('due_date'), '%Y-%m-%dT%H:%M:%SZ') if task.get('due_date') else timezone.now() + timedelta(days=1)
            due_date = timezone.make_aware(due_date, dt_timezone.utc)
            t = Task.objects.create(
                title=task.get('title', 'Untitled Task'),
                description=task.get('description', ''),
                due_date=due_date,
                priority=task.get('priority', Task.Priority.MEDIUM),
                tag=task.get('tag', 'general'),
                create_by='prompt'
            )
        status['status'] = {
            'status': 'success',
            'message': f"Task created successfully."
        }
        return f"Task created successfully."
    except json.JSONDecodeError as e:
        status['error'] = str(e)
        return f"Error generating task from text: {e}"
    finally:
        p.status = status
        p.save()