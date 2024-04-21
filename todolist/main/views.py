from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import TaskForm, TaskFormEdit
from .models import Task


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskFormEdit(instance=task)
    if request.method == 'POST':
        form = TaskFormEdit(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправление на список задач или другую страницу

    return render(request, 'main/edit_task.html', {'form': form})


class AddTaskView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'main/add_task.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Привязываем текущего пользователя к задаче
            task.save()
            return redirect('home')  # Перенаправляем пользователя на список задач
        return render(request, 'main/add_task.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('home')


def index(request):
    tasks = Task.objects.all()
    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'tasks': tasks})