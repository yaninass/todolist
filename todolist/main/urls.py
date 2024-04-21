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
]
