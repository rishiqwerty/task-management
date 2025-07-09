Backend Developer Assignment: The Engine for a Time-Aware Task API
Project Vision
Our goal is to create the backend service with python django for an intelligent task management application. This service will act as the "single source of truth" for any client application (web, mobile, etc.). You are responsible for building a robust, scalable, and secure REST API that handles all task management logic, including a key feature: automatically determining a task's status based on its deadline.
Your mission is to deliver a production-quality API engine that is reliable, well-tested, and well-documented, with a genuinely intelligent feature at its core.

Part 1: Core Features (The MVP)
Your first task is to build the Minimum Viable Product based on the following user stories.
User Story 1: Manual Task Management
"As a user, I want to create, view, update, and delete my tasks so I can manage my workload. I also need to be able to mark a task as 'complete' at any time."
User Story 2: Time-Aware Auto-Bucketing
"As a user, I want the application to automatically categorize my tasks based on their deadlines, so I can instantly see what's urgent, what I've accomplished, and what I've missed."
Tasks will automatically transition between three states, or "buckets":
Upcoming: The deadline is in the future and the task is not yet complete.
Completed: The task was manually marked as 'complete' by the user.
Missed: The deadline has passed and the task was not completed.


User Story 3: A Dynamic & Intuitive UI
"As a user, I want a clean, responsive, and real-time interface that provides immediate feedback on my actions and the status of my tasks without needing to refresh the page."
The UI should clearly separate the task buckets (e.g., using tabs, columns, or collapsible sections).
Users should receive instant visual feedback when a task's state changes (e.g., moving it to the 'Completed' bucket).
The design should be minimal, modern, and fully responsive for both desktop and mobile devices.


Part 2: The AI Innovation Challenge
This is where you will demonstrate your ability to integrate modern AI capabilities into a practical application. Your challenge is to implement one significant, AI-powered feature that makes the task management experience smarter for the end-user.
Requirement:
Choose one of the following options. You must add a new section to your README.md titled "AI Innovation Feature," explaining which option you chose, why it's valuable, your technical implementation (including which AI model/service you used), and how to use the new feature via the API.
Recommended Tooling: You can use any AI service you prefer. The OpenAI API (using a model like gpt-3.5-turbo) or the Hugging Face Inference API or Gemini 2.5 API are excellent choices for these tasks.

Evaluation Criteria & Submission
(The Evaluation and Submission sections remain the same, but now the "Innovation" criterion is explicitly about the quality and implementation of the chosen AI feature.)
Evaluation will heavily weigh:
The quality and correctness of your AI feature implementation.
The clarity of your README.md in explaining your AI choice and its implementation.
How well the new feature is integrated into the existing API structure.


SETUP
- Direnv
- poetry
- django
- drf