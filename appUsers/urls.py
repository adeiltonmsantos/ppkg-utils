from django.contrib.auth import views as auth_views
from django.urls import path  # type: ignore

from .forms import CustomLoginForm
from .views import UserRegistrationView

app_name = 'appUsers'

urlpatterns = [
    path(
        'login',
        auth_views.LoginView.as_view(
            template_name='appUsers/pages/login.html',
            authentication_form=CustomLoginForm
        ),
        name='login'
    ),
    path(
        'user_registration',
        UserRegistrationView.as_view(),
        name='user_registration'
    ),
]
