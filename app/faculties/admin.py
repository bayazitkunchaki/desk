from django.contrib import admin

from .models import Faculty, Group


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name',)
