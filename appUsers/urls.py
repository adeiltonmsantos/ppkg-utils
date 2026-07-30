from django.contrib.auth import views as auth_views
from django.urls import path  # type: ignore

app_name = 'appUsers'

urlpatterns = [
    path(
        'login',
        auth_views.LoginView.as_view(
            template_name='appUsers/pages/login.html'
        ),
        name='login'
    )
]
