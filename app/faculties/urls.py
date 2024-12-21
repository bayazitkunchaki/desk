from django.urls import path

from faculties import views

app_name = 'faculties'

urlpatterns = [
    path('', views.faculties_view, name='faculties_view'),
    path('<slug:faculty_slug>/courses/', views.faculty_courses, name='courses'),

]
