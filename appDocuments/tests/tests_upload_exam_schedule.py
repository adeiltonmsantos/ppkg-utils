from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class IntegrationTestUploadExamSchedule(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.url_exam_schedules = settings.BASE_DIR / 'utils/tests/timelines_to_test'
        return setup

    def loadPdfFile(self, pdf_name):
        pdf_url = self.url_exam_schedules / pdf_name
        with open(pdf_url, 'rb') as file:
            return SimpleUploadedFile(
                name=pdf_name,
                content=file.read(),
                content_type='application/pdf'
            )
    
    def test_if_file_is_valid(self):
        pdf_file = self.loadPdfFile('timeline_invalid.pdf')
        data = {'exam_schedule_pdf': pdf_file}
        
        resolve = self.client.post(
            reverse('appDocuments:upload-exam-schedule'),
            data=data,
            follow=True
        )

        self.assertIn(
            'O arquivo enviado não é válido',
            resolve.content.decode('utf-8')
        )