from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Введите имя"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Введите фамилию"}))
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Введите имя пользователя"}))
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={
        'class': "form-control", 'placeholder': "Введите электронную почту"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", 'readonly': True}),
                            required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"}))

    class Meta:
        model = User
        fields = ('username', 'password')

