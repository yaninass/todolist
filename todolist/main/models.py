from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    header = models.CharField(max_length=40)
    dispatcher = models.TextField(blank=True)
    isDo=models.BooleanField(default=False)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.header