from django.test import SimpleTestCase
from django.urls import reverse


class appUsersUrlTest(SimpleTestCase):
    def test_appUsers_login_url_is_correct(self):
        url = reverse('appUsers:login')
        url_wanted = '/users/login'
        self.assertEqual(
            url,
            url_wanted,
            msg=f'URL expected is "{url_wanted}" but "{url}" was found'
        )

    def test_appUsers_user_registration_is_correct(self):
        url = reverse('appUsers:user_registration')
        url_wanted = '/users/user_registration'
        self.assertEqual(
            url,
            url_wanted,
            msg=f'URL expected is "{url_wanted}" but "{url}" was found'
        )
