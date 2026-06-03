from django.test import SimpleTestCase
from django.urls import reverse


class appDocumentsUrlTest(SimpleTestCase):
    def test_appDocuments_home_url_is_correct(self):
        url = reverse('home')
        url_wanted = '/'
        self.assertEqual(url, url_wanted)

    def test_appDocuments_ipem_data_url_is_correct(self):
        url = reverse('appDocuments:ipem-data-send')
        url_wanted = '/documents/ipem_data/'
        self.assertEqual(url, url_wanted)
    
    def test_high_error_dispatch_url_is_correct(self):
        url = reverse('appDocuments:high-error-dispatch')
        url_wanted = '/documents/high-error-dispatch'
        self.assertEqual(url, url_wanted)
    
    def test_extract_exam_schedule_url_is_correct(self):
        url = reverse('appDocuments:extract-exam-schedule')
        url_wanted = '/documents/extract-exam-schedule'
        self.assertEqual(url, url_wanted)

