from collections import defaultdict

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import datetime, timedelta

from users.models import User
from users.utils import is_moderator_or_admin

from .forms import AddLessonForm, ScheduleForm
from .models import Group, Schedule


def group_schedule(request, group_slug):
    group = Group.objects.get(slug=group_slug)

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            today = datetime.today().date()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=4)
    except ValueError:
        today = datetime.today().date()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=4)

    schedule = Schedule.objects.filter(
        group=group,
        date__range=[start_date, end_date]
    ).order_by('date', 'pair_number')

    all_dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
        if (start_date + timedelta(days=i)).weekday() < 5
    ]

    grouped_schedule = defaultdict(list)
    for lesson in schedule:
        grouped_schedule[lesson.date].append(lesson)

    return render(request, 'timetable/group_schedule.html', {
        'grouped_schedule': grouped_schedule,
        'all_dates': all_dates,
        'title': f'Белгородский ГАУ - Расписание группы {group}',
        'group': group,
        'start_date': start_date,
        'end_date': end_date,
    })


def teacher_schedule(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    teacher_id = request.GET.get('teacher')

    schedules = Schedule.objects.all()

    if start_date:
        schedules = schedules.filter(date__gte=start_date)
    if end_date:
        schedules = schedules.filter(date__lte=end_date)
    if teacher_id:
        schedules = schedules.filter(teacher_id=teacher_id).order_by('date', 'pair_number')

    grouped_schedule = {}
    for schedule in schedules:
        grouped_schedule.setdefault(schedule.date, []).append(schedule)

    teachers = User.objects.all()

    return render(request, 'timetable/find_by_teacher.html', {
        'grouped_schedule': grouped_schedule,
        'teachers': teachers,
        'title': 'Белгородский ГАУ - Расписание преподавателей',
        'request': request,
    })


@login_required
@user_passes_test(is_moderator_or_admin)
def schedule_management(request):
    schedules = Schedule.objects.all()

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_management')
    else:
        form = ScheduleForm()

    return render(request, 'timetable/schedule_management.html', {
        'form': form,
        'schedules': schedules,
        'title': 'Белгородский ГАУ - Управление расписанием'
    })


@login_required
@user_passes_test(is_moderator_or_admin)
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule_management')
    else:
        form = ScheduleForm(instance=schedule)

    return render(request, 'timetable/edit_management.html', {'form': form, 'title': 'Белгородский ГАУ - '
                                                                                     'Редактирование расписания'})


@login_required
@user_passes_test(is_moderator_or_admin)
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    return redirect('schedule_management')


@login_required
@user_passes_test(is_moderator_or_admin)
def add_lesson(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    selected_date = request.GET.get('date', None)

    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.group = group
            if Schedule.objects.filter(pair_number=lesson.pair_number, group=group, date=lesson.date).exists():
                form.add_error('pair_number',
                               'Занятие с таким номером пары уже существует в данной группе на этот день.')

            if Schedule.objects.filter(pair_number=lesson.pair_number, teacher=lesson.teacher,
                                       date=lesson.date).exists():
                form.add_error('teacher', 'Преподаватель занят в этот день на эту пару.')
            else:
                try:
                    lesson.save()
                    return redirect('timetable:group_schedule', group_slug=group.slug)
                except IntegrityError as e:
                    print(f"Ошибка сохранения: {str(e)}")
                    form.add_error(None, 'Произошла ошибка при сохранении занятия.')
    else:
        form = AddLessonForm(initial={'date': selected_date})

    return render(request, 'timetable/add_lesson.html', {
        'form': form,
        'group': group,
        'selected_date': selected_date,
        'title': f'Белгородский ГАУ - Добавить занятие для группы {group.name}'
    })
