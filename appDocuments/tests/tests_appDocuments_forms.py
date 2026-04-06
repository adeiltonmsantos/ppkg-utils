import io
import os
import shutil
import tempfile

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
        # Creating the temporary folder
        cls.temp_media = tempfile.mkdtemp()

        # Data form
        cls.form_data = {
            'uf_ipem': 'AL',
            'sec_ipem': 'Secretaria',
            'rs_ipem': 'Instituto',
            'name_ppkg_ipem': 'Divisão de Pré-Embalados',
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
            'uf_ipem': 'AL',
            'sec_ipem': 'Secretaria de Estado',
            'rs_ipem': 'Instituto de Pesos e Medidas',
            'name_ppkg_ipem': 'Divisão de Pré-Embalados',
            'uf_img': '',
            'img_conv': ''
        }

        return super().setUp()

    def make_fake_image(self, img_name, size_mb=None):
        # Creating image in memory
        image = Image.new('RGB', (50, 50), color='green')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')

        return SimpleUploadedFile(
            f'{img_name}.jpg',
            img_io.getvalue(),
            content_type='image/jpeg'
        )
        # 1. Cria a imagem básica em memória
        # image = Image.new('RGB', (50, 50), color='green')
        # img_io = io.BytesIO()
        # image.save(img_io, format=img_format)

        # # 2. Se o parâmetro size_mb for passado, ajustamos o tamanho
        # if size_mb:
        #     target_size_bytes = int(size_mb * 1024 * 1024)
        #     current_size = img_io.tell() # Posição atual do cursor (tamanho atual)

        #     if target_size_bytes > current_size:
        #         # Adiciona a diferença em bytes nulos (\x00)
        #         remaining_bytes = target_size_bytes - current_size
        #         img_io.write(b'\0' * remaining_bytes)

        # # Captura o conteúdo final
        # content = img_io.getvalue()

        # return SimpleUploadedFile(
        #     name=f'{img_name}.{img_format.lower()}',
        #     content=content,
        #     content_type=f'image/{img_format.lower()}'
        # )

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
    ])
    def test_upload_of_images(self, field_name, img_name):
        # Creating fake image
        fake_image = self.make_fake_image('fake_image')

        self.form_data[field_name] = fake_image

        # URL of the view function that validate form
        url = reverse('appDocuments:ipem-data-receive')

        # Posting form with coat of arms image
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

        # Testing if form post without image erases it
        self.form_data[field_name] = ''

        # Posting form without coat of arms image
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
