from django.urls import path

from .views import UserLoginView, UserProfileView, UserRegistrationView, logout

app_name = 'users'

urlpatterns = [
    path('auth/', UserRegistrationView.as_view(), name='auth'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
]
