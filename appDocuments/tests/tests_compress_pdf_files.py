import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class IntegrationTestCompressPdfFiles(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT)
        super().tearDownClass()
                
    def setUp(self):
        setup = super().setUp()
        self.pdf_path = settings.BASE_DIR / 'utils/tests/pdf_to_test_compress'

        self.username = 'username'
        self.password = 'Abcd1234'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        self.client.login(
            username=self.username,
            password=self.password
        )

        return setup

    def loadFile(self, filename):
        fullpath = self.pdf_path / filename
        content = fullpath.read_bytes()

        return SimpleUploadedFile(
            name=filename,
            content=content,
            content_type='application/pdf'
        )

    def test_if_a_single_pdf_is_compressed(self):
        url = reverse('appDocuments:compress-pdf')
        pdffile = self.loadFile('file_test.pdf')
        data = {
            'main_filename': 'ARQUIVO',
            'pdf_files': pdffile
            }
        str_wanted = '<h3>Arquivos Compactados</h3>'
        response = self.client.post(
            url,
            data=data,
            follow=True
        )

        self.assertIn(
            str_wanted,
            response.content.decode('utf-8'),
            msg=f"String '{str_wanted}' not found"
        )
