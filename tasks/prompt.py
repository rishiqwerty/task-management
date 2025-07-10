from tasks.models import Task
from datetime import datetime
VALID_PRIORITIES = [choice.value for choice in Task.Priority]
LOCATION = '5:30'  # Example location offset for Kolkata, India
def generate_task_prioritization_prompt(relevant_tasks):
    if not relevant_tasks:
        task_list = "\n".join(
            [f"id:{t.id} Task: '{t.title}', Due: {t.due_date.strftime('%Y-%m-%d %H:%M')}, Description: {t.description or ''}, Existing Priority: {t.priority}" for t in relevant_tasks]
        )

        prompt = f"""
        You are a task prioritization assistant. Based on the following list of tasks, their deadlines, and descriptions, existing priorities, 
        please assign a priority and tag to each task.
        Based on the urgency and importance of these tasks, please
        assign a priority as one of these values only: {', '.join(VALID_PRIORITIES)}.
        And tag them with kind of task they are, like 'work', 'personal', 'urgent', etc.
        Respond with a single word for priority — one of: {', '.join(VALID_PRIORITIES)}. 
        And a tag for each task, like 'work', 'personal', 'urgent', etc.
        Tasks:
        {task_list}

        Return a JSON mapping task ids to their priority and tags.
        Important: Return a valid JSON object. 
        Keys must be enclosed in double quotes. 
        Values must be enclosed in double quotes (if strings) or valid JSON numbers. 
        Do not add extra spaces or new lines in the JSON object.
        Do not wrap your response in code block markers.
        """
    return prompt

def generate_task_from_text_prompt(text):
    prompt = f"""
    You are a task creation assistant. Based on the following text, create a task with the following fields:
    - Title
    - Description
    - Due Date (in UTC)
        - If no date is provided, use today's date "2025-07-10" and end of the day time "23:55" in Kolkata (Asia/Kolkata).
        - IMPORTANT: Convert all times to UTC.
        - Kolkata is UTC+5:30, so 23:55 in Kolkata is 18:25 UTC.
        - Apply this offset when converting any local time in the text to UTC.
        - Make sure time is in this format 2023-10-01T00:00:00Z
    - Priority (Guess the priority based on the text, and use the one mentioned based on the following values: {', '.join(VALID_PRIORITIES)}. 
        If not mentioned and you cant guess, default to 'medium')
    - Tag (Guess the tags if not mentioned, if not default to 'general')
    If the text does not contain enough information to create a task, return an empty JSON object.
    and if the text contains large amount of information, try creating multiple tasks.
    Text message: "{text}"
    Reminder:
    - If the text does not contain a due date, use today's date as the due date and set the time to 23:55 in Kolkata (Asia/Kolkata).
    - At last convert the due date to UTC that is -{LOCATION}.
    - If only time mentioned. then also subtract {LOCATION} from the time to convert it to UTC.
    Note Todays date is {datetime.now().strftime('%Y-%m-%d')}.
    Return a list of JSON object with the task details even if there is only one object.
    ex:
    {[{
        "title": "Task Title",
        "description": "Task Description",
        "due_date": "2023-10-01T00:00:00Z",
        "priority": "medium",
        "tag": "general"
    }]}
    Important: Return a valid JSON object. 
    Keys must be enclosed in double quotes. 
    Values must be enclosed in double quotes (if strings) or valid JSON numbers.
    Do not add extra spaces or new lines in the JSON object.
    Do not wrap your response in code block markers.
    """
    return prompt

import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemma-3-27b-it')

def gemini_api_call(prompt_text):
    response = model.generate_content(prompt_text)
    return response.text.strip()

import openai
from django.conf import settings


openai.api_key = settings.OPEN_AI_API_KEY
def openai_api_call(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
        )

    return response['choices'][0]['message']['content']