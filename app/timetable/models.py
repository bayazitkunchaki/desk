from django.db import models
from django.utils.text import slugify

from faculties.models import Faculty, Group
from users.models import User


class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField(max_length=512, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    LESSON_TYPE = [
        ('lecture', 'Лекция'),
        ('lab', 'Лабораторная работа'),
        ('seminar', 'Семинар'),
        ('practical', 'Практическая работа'),
        ('exam', 'Экзамен'),
        ('consultation', 'Консультация'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    pair_number = models.PositiveIntegerField()
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE)
    date = models.DateField()

    def __str__(self):
        return f'{self.subject} - {self.teacher} - {self.group} - {self.date} - Номер пары {self.pair_number}'

    class Meta:
        unique_together = ('pair_number', 'group', 'date')
