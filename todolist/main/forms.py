from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser, Task


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['header', 'dispatcher']


class TaskFormEdit(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['header', 'dispatcher', 'isDo']