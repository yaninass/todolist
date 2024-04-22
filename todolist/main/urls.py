from django.urls import path

from . import views
from .views import AddTaskView

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_task/', AddTaskView.as_view(), name='add_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('view-other-users-tasks/', views.view_other_users_tasks, name='view_other_users_tasks'),
    path('add-task-for-user/', views.add_task_for_user, name='add_task_for_user'),
]
