from django.urls import path
from .views import create_task, get_tasks, user_login, user_signup

urlpatterns = [
    path('create_task/', create_task, name='create_task'),
    path('get_tasks/', get_tasks, name='get_tasks'),
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='login_user'),
]