from django.contrib import admin

from .models import Schedule, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name',)


admin.site.register(Schedule)
