import io
import os
import shutil
import tempfile
from unittest.mock import patch

from django.conf import settings

# from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from parameterized import parameterized
from PIL import Image

# from forms import IpemDataRegisterForm
from appDocuments.forms.ipem_data_register import IpemDataRegisterForm


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
        # Creating the temporary media folder
        cls.temp_media = tempfile.mkdtemp()

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
            'uf_ipem': 'AL',
            'sec_ipem': 'Secretaria de Estado',
            'rs_ipem': 'Instituto de Pesos e Medidas',
            'name_ppkg_ipem': 'Divisão de Pré-Embalados',
            'uf_img': '',
            'uf_img_checkbox': False,
            'img_conv': '',
            'img_conv_checkbox': False,
            'img_signt': '',
            'img_signt_checkbox': False,
        }

        return super().setUp()

    def make_fake_image(self, img_name, size_mb=None):
        # 1. Cria a imagem básica em memória
        img_format = 'JPEG'
        image = Image.new('RGB', (50, 50), color='green')
        img_io = io.BytesIO()
        image.save(img_io, format=img_format)

        # 2. Se o parâmetro size_mb for passado, ajustamos o tamanho
        if size_mb:
            target_size_bytes = int(size_mb * 1024 * 1024)
            current_size = img_io.tell()  # Posição atual do cursor (tamanho atual)  # noqa: E501

            if target_size_bytes > current_size:
                # Adiciona a diferença em bytes nulos (\x00)
                remaining_bytes = target_size_bytes - current_size
                img_io.write(b'\0' * remaining_bytes)

        # Captura o conteúdo final
        content = img_io.getvalue()

        return SimpleUploadedFile(
            name=f'{img_name}.{img_format.lower()}',
            content=content,
            content_type=f'image/{img_format.lower()}'
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

    @parameterized.expand([
        ('img_uf', 'brasao.png'),
        ('img_conv', 'convenio.png'),
        ('img_signt', 'assinatura.png'),
    ])
    def test_upload_of_images(self, field_name, img_name):
        # Creating fake image
        fake_image = self.make_fake_image('fake_image')

        self.form_data[field_name] = fake_image

        # URL of the view function that validate form
        url = reverse('appDocuments:ipem-data-receive')

        # Posting form with image
        self.client.post(
            url,
            data=self.form_data,
            follow=True,
            format='multipart'
        )

        # Testing if image exists
        file_exists = os.path.exists(settings.MEDIA_ROOT + f'/{img_name}')  # noqa:E501

        self.assertTrue(
            file_exists,
            msg=f"File '{img_name}' doesn't exist"
        )

    @parameterized.expand([
        ('img_uf', 'img_uf_checkbox', 'brasao.png'),
        ('img_conv', 'img_conv_checkbox', 'convenio.png'),
        ('img_signt', 'img_signt_checkbox', 'assinatura.png'),
    ])
    def test_if_image_is_deleted(self, field_name, field_delete_name, img_name):
        # URL of the view function that validate form
        url = reverse('appDocuments:ipem-data-receive')

        # Creating a fake image
        fake_image = self.make_fake_image('fake_image')

        # Saving image via post
        self.form_data[field_name] = fake_image
        self.client.post(
            url,
            data=self.form_data,
            follow=True,
            format='multipart'
        )

        # Testing if form post without image erases it
        self.form_data[field_name] = ''
        self.form_data[field_delete_name] = True

        # Trying to delete image via POST
        self.client.post(
            url,
            data=self.form_data,
            follow=True,
            format='multipart'
        )

        # Testing if image doesn't exist
        file_exists = os.path.exists(settings.MEDIA_ROOT + f'/{img_name}')  # noqa:E501

        self.assertFalse(file_exists)

    @parameterized.expand([
        ('img_uf', 'O tamanho da imagem do brasão do estado não pode ser maior que 3MB'),  # noqa: E501
        ('img_conv', 'O tamanho da imagem do convênio INMETRO/IPEM não pode ser maior que 3MB'),  # noqa: E501
        ('img_signt', 'O tamanho da imagem do responsável não pode ser maior que 3MB'),  # noqa: E501
    ])
    def test_if_size_of_images_are_allowed(self, field_name, msg_wanted):
        # Creating fake image
        fake_image = self.make_fake_image('fake_image', 4)

        self.form_data[field_name] = fake_image

        # URL of the view function that validate form
        url = reverse('appDocuments:ipem-data-receive')

        # Posting form with coat of arms image
        resolve = self.client.post(
            url,
            data=self.form_data,
            follow=True,
            format='multipart'
        )

        self.assertIn(msg_wanted, resolve.content.decode('utf-8'))

    @parameterized.expand([
        ('uf_ipem', 'Selecione um estado'),
        ('sec_ipem', 'O nome da secretaria deve ter no mínimo 10 caracteres'),
        ('rs_ipem', 'A razão social do IPEM deve ter no mínimo 10 caracteres'),
        ('name_ppkg_ipem', 'O nome do setor de pré-embalados deve ter no mínimo 10 caracteres'),  # noqa: E501
        ('img_uf', 'A imagem do brasão do estado não deve ser superior a 3 MB'),  # noqa: E501
        ('img_conv', 'A imagem do convênio INMETRO/IPEM não deve ser superior a 3MB'),  # noqa: E501
    ])
    def test_error_messages_fields_are_correct(self, field_name, message):
        if field_name in ('img_uf', 'img_conv'):
            pass
        else:
            self.form_data[field_name] = '  '
            # URL of the view function that validate form
            url = reverse('appDocuments:ipem-data-receive')

            # Posting data
            response = self.client.post(
                url,
                data=self.form_data,
                follow=True,
                format='multipart'
            )

            self.assertIn(
                message,
                response.content.decode('utf-8'),
                msg=f'"{field_name}" error message mus be "{message}"'
            )

    @patch(
            'appDocuments.forms.ipem_data_register.JSON_PATH',
            new='non_existing_folder/'
    )
    def test_if_json_file_exists(self):
        url = reverse('appDocuments:ipem-data-receive')
        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,
            format='multipart'
        )
        self.assertIn(
            'Os dados do IPEM não foram salvos',
            response.content.decode('utf-8')
        )
