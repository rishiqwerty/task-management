# Task Management Platform

## Project Vision
A robust, scalable, and intelligent task management backend (Django) and frontend (React) with real-time UI, AI-powered features, and easy deployment via Docker.

---

## Features
- **Task CRUD**: Create, view, update, delete, and complete tasks
- **Time-Aware Bucketing**: Tasks auto-categorized as Upcoming, Completed, or Missed
- **Priority & Tags**: AI or user-assigned, with visual badges
- **Real-Time UI**: Instant feedback, transitions, and polling
- **AI Text-to-Task**: Generate tasks from natural language
- **Responsive Frontend**: Modern, mobile-friendly React + MUI
- **Dockerized**: One-command setup for backend, Celery, Redis

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rishiqwerty/task-management.git
cd task_management
```

### 2. Backend Setup (Django)
#### a. Environment Variables
- Copy the example env file and edit as needed:
  ```bash
  cd task_management
  cp env.example .env
  # Edit .env with your secrets and config
  ```

#### b. Docker Compose (Recommended)
```bash
docker compose up --build
```
- Backend API: http://localhost:9000
- API Docs: http://localhost:9000/api/schema/swagger-ui/

#### c. Local Dev (Optional)
- Install Poetry: https://python-poetry.org/docs/#installation
- Install dependencies:
  ```bash
  poetry install
  poetry run python manage.py migrate
  poetry run python manage.py runserver
  ```

### 3. Frontend Setup (React)
clone Frontend repo:
- git clone https://github.com/rishiqwerty/task-management-frontend.git

```bash
cd ../task-management-frontend
npm install
npm run dev
```
- Frontend: http://localhost:5173

---

## Environment Variables (.env)
- See `task_management/env.example` for all options
- Lists (e.g. ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS) are comma-separated
- Example:
  ```env
  DEBUG=True
  SECRET_KEY=your-secret-key
  ALLOWED_HOSTS=localhost,127.0.0.1
  CORS_ALLOWED_ORIGINS=http://localhost:5173
  CELERY_BROKER_URL=redis://redis:6379/0
  CELERY_RESULT_BACKEND=redis://redis:6379/0
  OPENAI_API_KEY=sk-...
  ```

---

## AI Innovation Feature

**Text-to-Task** allows users to describe a project, goal, or task list in natural language. The backend service (powered by OpenAI/Gemini — currently using OpenAI) intelligently parses the text into structured, actionable tasks with auto-assigned:

- **Titles**
- **Descriptions**
- **Due dates**
- **Priorities** (inferred from text context)
- **Tags** (classified based on content)

📌 **API Endpoint:**
```
POST /tasks/tasks/text_to_task_action/
```

📌 **Request Body Example:**
```json
{
  "text": "I'm planning to build an expense tracking app. First, set up the database by tomorrow. Then design the UI this week. Prepare a presentation by next Monday."
}
```

📌 **How it works:**
- The backend uses an AI model to:
  - Parse the input text.
  - Detect multiple distinct tasks.
  - Assign inferred priorities and tags if unspecified.
  - Set due dates based on detected time references (with automatic conversion to UTC).
  - Create and save each task to the database.

📌 **Frontend Integration:**
A "Create Tasks from Text" input is available at the top of the UI for users to quickly describe their workload in natural language.

---

## Development
- **Backend**: Django, DRF, Celery, Redis, Poetry
- **Frontend**: React, MUI, Axios
- **AI**: OpenAI or Gemini

---

## Troubleshooting
- **Docker Compose**: Use `docker compose` (not `docker-compose`)
- **Celery/Redis**: Ensure Redis is running and env vars use `redis://redis:6379/0` in docker and `redis://redis:6379/0` for local development
- **Frontend CORS**: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`

---

## Future Enhancements

- **User Authentication & Profiles**: Add user accounts, login, and per-user task lists
- **OAuth & Social Login**: Google, GitHub, etc.
- **Push Notifications**: Email, SMS, or browser notifications for deadlines and reminders
- **Recurring Tasks**: Support for tasks that repeat on a schedule
- **Sub Tasks**: Create sub task of a main task
- **Team Collaboration**: Assign tasks to multiple users, comments, and activity logs




