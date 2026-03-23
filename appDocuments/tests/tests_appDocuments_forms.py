import io
import shutil
import tempfile

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from parameterized import parameterized
from PIL import Image

from appDocuments.forms import IpemDataRegisterForm
from utils.django_midia import saveImageAsPng


class AppDocumentsTestForm(TestCase):
    @parameterized.expand([
        ('sec_ipem', 'Ex.: Secretaria de Estado de Ind. e Comércio'),
        ('rs_ipem', 'Ex.: Inst. de Metrologia e Qualidade de Alagoas'),
        ('name_ppkg_ipem', 'Ex.: Divisão de Pré-Embalados'),
    ])
    def test_placeholders_fields_are_correct(self, field, placeholder):
        form = IpemDataRegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(
            current_placeholder,
            placeholder,
            msg=f'Wanted {placeholder} but found {current_placeholder}'
        )

    @parameterized.expand([
        ('uf_ipem', 'O campo "Estado do IPEM" é obrigatório'),
        ('sec_ipem', 'A "Secretaria" ao qual o IPEM é vinculado é obrigatória'),  # noqa: E501
        ('rs_ipem', 'A "Razão Social" do IPEM é obrigatória'),
        ('name_ppkg_ipem', 'A "Nome" do setor de Pré-Embalados é obrigatório'),
    ])
    def test_message_errors_fields_are_correct(self, field, error_msg):
        form = IpemDataRegisterForm()
        current_error_msg = form[field].field.error_messages['required']
        self.assertEqual(
            current_error_msg,
            error_msg,
            msg=f'Wanted {error_msg} but found {current_error_msg}'
        )


class AppDocumentsIntegrationTestForm(TestCase):
    @classmethod
    def setUpClass(cls):
        # Creating the temporary folder
        cls.temp_media = tempfile.mkdtemp()

        # Data form
        cls.form_data = {
            'uf_ipem': 'Alagoas',
            'sec_ipem': 'Secretaria',
            'rs_ipem': 'Instituto',
            'name_ppkg_ipem': 'Divisão',
            'uf_img': None,
            'img_conv': None
        }

        # Overwriting MEDIA_ROOT url
        cls.override = override_settings(MEDIA_ROOT=cls.temp_media)
        cls.override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        # Deactivating the override of MEDIA_ROOT
        cls.override.disable()

        # Erasing temporary midia folder
        shutil.rmtree(cls.temp_media, ignore_errors=True)

    def setUp(self):
        # Data form
        self.form_data = {
            'uf_ipem': 'Alagoas',
            'sec_ipem': 'Secretaria',
            'rs_ipem': 'Instituto',
            'name_ppkg_ipem': 'Divisão',
            'uf_img': None,
            'img_conv': None
        }

        return super().setUp()

    def make_fake_image(self, img_name, img_format='PNG'):
        # Creating image in memory
        image = Image.new('RGB', (50, 50), color='green')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')

        return SimpleUploadedFile(
            f'{img_name}.jpg',
            img_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_uf_field_must_be_selected(self):
        # Defining invalid value to uf fielf
        self.form_data['uf_ipem'] = ' '

        # URL of the view function that validate form
        url = reverse('appDocuments:ipem-data-receive')

        # Posting form
        resolve = self.client.post(url, data=self.form_data, follow=True)

        # Wanted error message about uf field
        msg_wanted = 'Selecione um estado'

        # Testing...
        self.assertIn(
            msg_wanted,
            resolve.content.decode('utf-8')
        )

    def test_if_coat_of_arms_image_is_deleted_if_no_upload_is_done(self):
        # URL of the view function that validate form
        url = reverse('appDocuments:ipem-data-receive')

        # Creating fake image
        fake_image = self.make_fake_jpg_image('fake_image')

        # Saving fake image in temporary midia folder
        saveImageAsPng(fake_image, 'brasao')

        # Posting form
        # resolve = self.client.post(url, data=self.form_data, follow=True)

        pass
        # Getting names of images by form posted
        # brasao_img_name = resolve.context['form']
