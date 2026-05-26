from unittest import TestCase

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from utils.fpdf import PDF


class UnitTestPDF(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.conv_path = settings.BASE_DIR / 'utils/tests/imgs_to_test/convenio.png'
        return setup
    
    def test_if_image_is_rendered_correctly(self):
        # Getting URL of image
        url = self.conv_path

        # Trying to load to memory a PDF file to test
        imagefile = None
        try:
            with open(url, 'rb') as f:
                img_file = f.read()
            imagefile = SimpleUploadedFile(
                name='convenio.png',
                content=img_file,
                content_type='image/png'
            )
        except Exception:
            print('aguma coisa deu errado')

        # Instantiating a PDF file
        pdf = PDF()
        pdf.renderImage(imagefile, align='C', opacity=0.2)
        pdf.output('test.pdf')
        # Inserting the image in center of page