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
