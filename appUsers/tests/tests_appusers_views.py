from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import resolve, reverse


class appUsersViewsTest(SimpleTestCase):

    def test_ipem_data_based_function_view_is_correct(self):
        resolve_obj = resolve(reverse('appUsers:login'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = auth_views.LoginView
        self.assertIs(bcv, bcv_wanted)
