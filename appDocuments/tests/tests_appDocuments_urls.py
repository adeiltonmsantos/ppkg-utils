from django.test import TestCase
from django.urls import reverse


class appDocumentsUrlTest(TestCase):
    def test_appDocuments_home_url_is_correct(self):
        url = reverse('appDocuments:home')
        url_wanted = '/documents/home/'
        self.assertEqual(url, url_wanted)
