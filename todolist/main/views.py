from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import TaskForm, TaskFormEdit, AddTaskToUserForm
from .models import Task


def view_other_users_tasks(request):
    tasks = Task.objects.exclude(user__is_superuser=True)
    return render(request, 'main/other_users_tasks.html', {'tasks': tasks})


def add_task_for_user(request):
    if request.method == 'POST':
        form = AddTaskToUserForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('view_other_users_tasks')
    else:
        form = AddTaskToUserForm()
    return render(request, 'main/add_task_for_user.html', {'form': form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskFormEdit(request.POST, instance=task)
        if form.is_valid():
            form.save()

            if request.user.is_superuser and task.user != request.user:
                redirect_url = 'view_other_users_tasks'
            else:
                redirect_url = 'home'
            return redirect(redirect_url)
    else:
        form = TaskFormEdit(instance=task)

    return render(request, 'main/edit_task.html', {'form': form})


class AddTaskView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'main/add_task.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
        return render(request, 'main/add_task.html', {'form': form})


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        if request.user.is_superuser and task.user != request.user:
            redirect_url = 'view_other_users_tasks'
        else:
            redirect_url = 'home'
        return redirect(redirect_url)
    return redirect('home')


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

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
            # Check for specific errors and display corresponding error messages
            if 'username' in form.errors:
                error_message = form.errors['username'][0]
                messages.error(request, f'Ошибка: {error_message}')
            if 'password1' in form.errors:
                error_message = form.errors['password1'][0]
                messages.error(request, f'Ошибка: {error_message}')
            if 'password2' in form.errors:
                error_message = form.errors['password2'][0]
                messages.error(request, f'Ошибка: {error_message}')
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
    undone_tasks = Task.objects.filter(isDo=False).order_by('-pk')
    done_tasks = Task.objects.filter(isDo=True).order_by('-pk')
    tasks = list(undone_tasks) + list(done_tasks)
    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'tasks': tasks})
