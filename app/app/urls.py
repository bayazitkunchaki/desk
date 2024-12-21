from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app import settings
from faculties.views import index_view
from timetable.views import (delete_schedule, edit_schedule,
                             schedule_management, teacher_schedule)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', index_view, name='index'),
    path('faculties/', include('faculties.urls', namespace='faculties')),
    path('groups/', include('timetable.urls', namespace='timetable')),
    path('teacher_schedule/', teacher_schedule, name='teacher_schedule'),

    path('schedule_management/', schedule_management, name='schedule_management'),
    path('edit_schedule/<int:schedule_id>/', edit_schedule, name='edit_schedule'),
    path('delete_schedule/<int:schedule_id>/', delete_schedule, name='delete_schedule'),

]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
