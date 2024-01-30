from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from api.tasks import print_task
from .models import Task
from django.utils import timezone
import json
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from api.serializers import UserSerializer
from functools import wraps
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully.'})
    else:
        return Response(serializer.errors, status=400)
    

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful.'})
    else:
        return Response({'error': 'Invalid credentials please provide valid credentials.'}, status=401)
    
     
@require_POST    
@csrf_exempt
@login_required
def create_task(request):
    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
            task_name = data.get('task_name')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in the request body.'}, status=400)

        if not task_name:
            return JsonResponse({'error': 'Task name is required.'}, status=400)
        #Scheduled task creation 
        print_task.apply_async(args=[task_name], countdown=600)

        new_task = Task.objects.create(user=request.user, task_name=task_name)

        response_data = {
            'message': f"Task '{task_name}' created successfully at {timezone.now()}.",
            'task': {
                'id': new_task.id,
                'task_name': new_task.task_name,
                'created_at': new_task.created_at,
            },
        }
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_GET
@csrf_exempt
def get_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    task_names = [task.task_name for task in user_tasks]
    return JsonResponse({"tasks": task_names})