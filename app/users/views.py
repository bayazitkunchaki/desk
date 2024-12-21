from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from faculties.mixins import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import User


class UserLoginView(SuccessMessageMixin, TitleMixin, LoginView):
    form_class = UserLoginForm
    title = 'Белгородский ГАУ - Вход'

    def get(self, request, *args, **kwargs):
        return redirect('users:auth')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    title = 'Белгородский ГАУ - Вход'
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_message = 'Вы успешно зарегистрировались. Войдите'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserProfileView(LoginRequiredMixin, TitleMixin,  UpdateView):
    title = 'Белгородский ГАУ - Профиль'
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user



@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))
