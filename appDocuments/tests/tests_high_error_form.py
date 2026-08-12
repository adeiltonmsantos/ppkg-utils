import datetime as dt
from datetime import timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from utils.fpdf import PDF

User = get_user_model()

class IntegrationTestHighErrorDispatch(TestCase):
    def make_pdf(self):
        pdf = PDF()
        return pdf.output(dest='S')

    def setUp(self):
        # Standard data for form
        self.form_data = {
            'dispatch_date': f'{dt.datetime.now(tz=timezone.utc).day}/{dt.datetime.now(tz=timezone.utc).month}/{dt.datetime.now(tz=timezone.utc).year}',
            'dispatch_pdf': '',
        }
        self.test_reports_path = settings.BASE_DIR / 'utils/tests/reports_to_test'

        # Creating and authenticating user
        self.username = 'Usuario'
        self.password = '123StrongPassword'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client.login(
            username=self.username,
            password=self.password
        )

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
        except FileNotFoundError:
            return False

    def test_high_error_dispatch_loads_errors_from_pdf_files(self):
        self.form_data['dispatch_pdf'] = [
                    self.loadExamReportPDF('ld_high_rp_01.pdf'),
                    self.loadExamReportPDF('ld_length_rp_01.pdf'),
                    self.loadExamReportPDF('ld_mass_rp_01.pdf'),
                    self.loadExamReportPDF('ld01.pdf'),
        ]
        
        resolve = self.client.post(
            reverse('appDocuments:high-error-dispatch'),
            data=self.form_data,
            follow=True
        )
        
        str_wanted = '</a> para baixar o despacho'
        self.assertIn(
            str_wanted,
            resolve.content.decode('utf-8'),
            msg=f'Wanted string "{str_wanted}" not found'
        )

    def test_high_error_dispatch_displays_message_if_theres_no_error(self):
        self.form_data['dispatch_pdf'] = [
                    self.loadExamReportPDF('ld_unid_rp_02.pdf'),
        ]
        
        resolve = self.client.post(
            reverse('appDocuments:high-error-dispatch'),
            data=self.form_data,
            follow=True
        )
        
        str_wanted = 'Não há erros para geração de despacho no(s) arquivo(s) enviado(s)'
        self.assertIn(
            str_wanted,
            resolve.content.decode('utf-8'),
            msg=f'Wanted string "{str_wanted}" not found'
        )

    def test_high_error_dispatch_displays_warns_about_invalid_file(self):
        self.form_data['dispatch_pdf'] = [
                    self.loadExamReportPDF('ld_unid_rp_02.pdf'),
                    self.loadExamReportPDF('ld_invalid_01.pdf'),
        ]
        
        resolve = self.client.post(
            reverse('appDocuments:high-error-dispatch'),
            data=self.form_data,
            follow=True
        )
        
        str_wanted = 'Arquivo(s) inválido(s) encontrado(s):'
        self.assertIn(
            str_wanted,
            resolve.content.decode('utf-8'),
            msg=f'Wanted string "{str_wanted}" not found'
        )
