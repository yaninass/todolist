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


class AddTaskToUserForm(forms.Form):
    user = forms.ModelChoiceField(label='User', queryset=CustomUser.objects.all())
    header = forms.CharField(label='Header', max_length=40)
    dispatcher = forms.CharField(label='Dispatcher', widget=forms.Textarea, required=False)


    def save(self):
        user = self.cleaned_data['user']
        header = self.cleaned_data['header']
        dispatcher = self.cleaned_data['dispatcher']
        task = Task.objects.create(user=user, header=header, dispatcher=dispatcher)
        return task