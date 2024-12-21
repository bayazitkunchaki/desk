from django.contrib.auth.models import AbstractUser
from django.db import models

from faculties.models import Faculty, Group


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('moderator', 'Составитель')
    )
    role = models.CharField(max_length=64, choices=ROLE_CHOICES, default='student')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.role}'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
