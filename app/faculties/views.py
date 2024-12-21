from django.shortcuts import get_object_or_404, render

from .models import Faculty, Group


def index_view(request):
    return render(request, 'faculties/index.html', {'title': 'Расписание Белгородский ГАУ'})


def faculties_view(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculties/faculties.html', {'faculties': faculties, "title": 'Белгородский ГАУ - Факультеты'})


def faculty_courses(request, faculty_slug):
    faculty = get_object_or_404(Faculty, slug=faculty_slug)
    course = request.GET.get('course')
    if course:
        groups = Group.objects.filter(faculty=faculty, course=course)
    else:
        groups = Group.objects.filter(faculty=faculty)

    return render(request, 'faculties/faculty_courses.html', {'faculty': faculty, 'groups': groups, 'title': 'Белгородский ГАУ - Группы'})
