from django.test import SimpleTestCase
from django.urls import resolve, reverse

from appDocuments import views


class appDocumentsViewsTest(SimpleTestCase):

    def test_appDocuments_ipem_data_view_is_correct(self):
        view = resolve(reverse('appDocuments:ipem-data'))
        self.assertIs(view.func, views.ipemData)

    def test_appDocuments_ipem_data_template_is_correct(self):
        response = self.client.get(reverse('appDocuments:ipem-data'))
        self.assertTemplateUsed(response, 'appDocuments/pages/ipem_data.html')