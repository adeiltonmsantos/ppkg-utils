import datetime as dt

from django.test import TestCase
from django.urls import reverse

from utils.fpdf import PDF


class IntegrationTestHighErrorDispatch(TestCase):
    def make_pdf(self):
        pdf = PDF()
        return pdf.output(dest='S')

    def setUp(self):
        self.form_data = {
            'dispatch_date': '',
            'dispatch_pdf': self.make_pdf()
        }
        return super().setUp()

    def test_high_error_dispatch_validate_date(self):
        url = reverse('appDocuments:high-error-dispatch')
        self.form_data['dispatch_date'] = '1/1/0001'
        resolve = self.client.post(url, data=self.form_data, follow=True, format='multipart')

        self.assertIn(
            'A data informada é inválida',
            resolve.content.decode('utf-8')
        )