from django.test import SimpleTestCase
from parameterized import parameterized

from appDocuments.forms import IpemDataRegisterForm


class AppDocumentsTestForm(SimpleTestCase):
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


class AppDocumentsIntegrationTestForm(SimpleTestCase):
    def setUp(self):
        self.form_data = {
            'uf_ipem': 'Alagoas',
            'sec_ipem': 'Secretaria',
            'rs_ipem': 'Instituto',
            'name_ppkg_ipem': 'Divisão',
        }
        return super().setUp()

    def test_uf_field_must_be_selected(self):
        self.form_data['uf_ipem'] = ' '
        form = IpemDataRegisterForm(self.form_data)
        url = ''