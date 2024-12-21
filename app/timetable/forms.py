from django import forms

from users.models import User

from .models import Schedule


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'teacher', 'group', 'pair_number', 'lesson_type', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'teacher', 'lesson_type', 'date', 'pair_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher'].widget.attrs.update({'class': 'form-control'})
        self.fields['lesson_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['pair_number'].widget.attrs.update({'class': 'form-control'})

        self.fields['teacher'].queryset = User.objects.filter(role='teacher')
