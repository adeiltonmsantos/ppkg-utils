from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from appUsers.views import UserRegistrationView


class appUsersViewsTest(SimpleTestCase):

    def test_appUser_ipem_data_CBV_is_correct(self):
        resolve_obj = resolve(reverse('appUsers:login'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = auth_views.LoginView
        self.assertIs(bcv, bcv_wanted)

    def test_appUser_user_registration_CBV_is_correct(self):
        resolve_obj = resolve(reverse('appUsers:user_registration'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = UserRegistrationView
        self.assertIs(bcv, bcv_wanted)
