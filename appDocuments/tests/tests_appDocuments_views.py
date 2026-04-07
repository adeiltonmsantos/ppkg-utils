from django.test import SimpleTestCase
from django.urls import resolve, reverse

from appDocuments import views


class appDocumentsViewsTest(SimpleTestCase):

    def test_appDocuments_ipem_data_based_function_view_is_correct(self):
        resolve_obj = resolve(reverse('appDocuments:ipem-data-send'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = views.IpemData
        self.assertIs(bcv, bcv_wanted)

    def test_appDocuments_ipem_data_template_is_correct(self):
        response = self.client.get(reverse('appDocuments:ipem-data-send'))
        self.assertTemplateUsed(response, 'appDocuments/pages/ipem_data.html')
