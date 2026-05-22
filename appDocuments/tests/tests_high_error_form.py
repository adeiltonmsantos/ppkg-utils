import datetime as dt

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from utils.fpdf import PDF


class IntegrationTestHighErrorDispatch(TestCase):
    def make_pdf(self):
        pdf = PDF()
        return pdf.output(dest='S')

    def setUp(self):
        self.form_data = {
            'dispatch_date': f'{dt.datetime.today().day}/{dt.datetime.today().month}/{dt.datetime.today().year}',  # noqa:E501
            'dispatch_pdf': '',
        }
        self.test_reports_path = settings.BASE_DIR / 'utils/tests/reports_to_test'
        return super().setUp()

    def loadExamReportPDF(self, pdf_name):
        """
        loadExamReportPDF(pdf_name)
        Returns a PDF file object in memory based on the name of a PDF in utils/tests/reports_to_test.
        If file doesn't exist returns False
        """
        # Exam report path to test
        pdf_path = self.test_reports_path / pdf_name

        # Trying to load to memory a PDF file to test
        try:
            with open(pdf_path, 'rb') as f:
                pdf_file = f.read()
            return SimpleUploadedFile(
                name=pdf_name,
                content=pdf_file,
                content_type='application/pdf'
            )
        except Exception:
            return False

    def test_high_error_dispatch_validate_date(self):
        url = reverse('appDocuments:high-error-dispatch')
        self.form_data['dispatch_date'] = '1/1/0001'
        resolve = self.client.post(url, data=self.form_data, follow=True, format='multipart')

        self.assertIn(
            'A data informada é inválida',
            resolve.content.decode('utf-8')
        )

    def test_high_error_dispatch_loads_errors_from_pdf_files(self):
        self.form_data['dispatch_pdf'] = [
                    self.loadExamReportPDF('ld_high_rp_01.pdf'),
                    self.loadExamReportPDF('ld_length_rp_01.pdf'),
                    self.loadExamReportPDF('ld_mass_rp_01.pdf'),
        ]
        
        resolve = self.client.post(
            reverse('appDocuments:high-error-dispatch'),
            data=self.form_data,
            # format='multpart',
            follow=True
        )
        pass