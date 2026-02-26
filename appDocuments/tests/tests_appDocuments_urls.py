from django.test import SimpleTestCase
from django.urls import reverse


class appDocumentsUrlTest(SimpleTestCase):
    def test_appDocuments_home_url_is_correct(self):
        url = reverse('appDocuments:home')
        url_wanted = '/documents/home/'
        self.assertEqual(url, url_wanted)

    def test_appDocuments_ipem_data_url_is_correct(self):
        url = reverse('appDocuments:ipem-data')
        url_wanted = '/documents/ipem_data/'
        self.assertEqual(url, url_wanted)
