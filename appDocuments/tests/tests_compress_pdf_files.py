from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class IntegrationTestCompressPdfFiles(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.url_exam_schedules = settings.BASE_DIR / 'utils/tests/pdf_to_test_compress'
        return setup

    def loadPdfFile(self, pdf_name):
        pdf_url = self.url_exam_schedules / pdf_name
        with open(pdf_url, 'rb') as file:
            return SimpleUploadedFile(
                name=pdf_name,
                content=file.read(),
                content_type='application/pdf'
            )
