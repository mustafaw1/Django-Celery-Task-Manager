# Django-Celery-Task-Manager

# Running the Project

1. Build and start containers:

Bash
docker-compose up --build
2. Access the Django application:

Open your web browser and visit: http://localhost:8000/
# API Endpoints

## Signup

Endpoint: /api/signup/

Method: POST

Payload:

JSON
{
  "username": "your_username",
  "password": "your_password"
}
## Login

Endpoint: /api/login/

Method: POST

Payload:

JSON
{
  "username": "your_username",
  "password": "your_password"
}

Response: Receive a JWT token.

## Create Task

Endpoint: /api/create_task/

Method: POST

Headers: Authorization: Bearer <your_token>

Payload:

JSON
{
  "task_name": "your_task_name"
}

## Get Tasks

Endpoint: /api/get_tasks/
Method: GET
Headers: Authorization: Bearer <your_token>
# Scheduled Tasks with Celery

## Start Celery Worker:

Bash
pipenv run celery -A SelteqTask worker -l info

## Schedule Task:

Use the /api/create_task/ endpoint to schedule a task with a specific time.