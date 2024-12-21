from django.urls import path

from . import views

app_name = 'timetable'

urlpatterns = [

    path('<slug:group_slug>/', views.group_schedule, name='group_schedule'),
    path('<slug:group_slug>/add_lesson/', views.add_lesson, name='add_lesson'),
]
