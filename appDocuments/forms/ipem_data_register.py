from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    # 3MB em bytes
    if filesize > 3 * 1024 * 1024:
        raise ValidationError("A imagem não pode ser maior que 3MB.")
    return value


def is_num_characters_valid(value, num_chars_valid):
    is_valid = len(str(value).strip()) >= num_chars_valid
    return is_valid


class IpemDataRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors_fields = defaultdict(list)

    uf_choices = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espirito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MS': 'Mato Grosso do Sul',
        'MT': 'Mato Grosso',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }

    uf_ipem = forms.ChoiceField(
        label='Estado do IPEM',
        choices={' ': 'Selecione um estado', **uf_choices},
        error_messages={
            'required': 'O campo "Estado do IPEM" é obrigatório'
        },
    )

    sec_ipem = forms.CharField(
        label='Secretaria de Estado ao qual o IPEM é vinculado',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Secretaria de Estado de Ind. e Comércio',
            'class': 'form-text-input'
        }),
        error_messages={
            'required': 'A "Secretaria" ao qual o IPEM é vinculado é obrigatória'  # noqa: E501
        }
    )

    rs_ipem = forms.CharField(
        label='Razão Social do IPEM',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Inst. de Metrologia e Qualidade de Alagoas',
            'class': 'form-text-input'
        }),
        error_messages={
            'required': 'A "Razão Social" do IPEM é obrigatória'
        }
    )

    name_ppkg_ipem = forms.CharField(
        label='Nome do setor de Pré-Embalados',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Divisão de Pré-Embalados',
            'class': 'form-text-input'
        }),
        error_messages={
            'required': 'A "Nome" do setor de Pré-Embalados é obrigatório'
        }
    )

    img_uf = forms.FileField(
        required=False,
        label='Imagem do brasão do estado',
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'accept': 'image/*'
        }),
    )

    img_conv = forms.FileField(
        required=False,
        label='Imagem do convênio INMETRO/IPEM',
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'accept': 'image/*'
        }),
    )

    def clean(self):
        super_clean = super().clean()

        cleaned_data = self.cleaned_data
        uf_ipem = cleaned_data.get('uf_ipem')
        sec_ipem = cleaned_data.get('sec_ipem')
        rs_ipem = cleaned_data.get('rs_ipem')
        name_ppkg_ipem = cleaned_data.get('name_ppkg_ipem')
        img_uf = self.files.get('img_uf')
        img_conv = self.files.get('img_conv')

        # Validating uf_ipem
        if len(str(uf_ipem).strip()) == 0:
            self.errors_fields['uf_ipem'].append('Selecione um estado')

        # Validating sec_ipem
        if not is_num_characters_valid(sec_ipem, 10):
            self.errors_fields['sec_ipem'].append('O nome da secretaria deve ter no mínimo 10 caracteres')  # noqa: E501

        # Validating rs_ipem
        if not is_num_characters_valid(rs_ipem, 10):
            self.errors_fields['rs_ipem'].append('A razão social do IPEM deve ter no mínimo 10 caracteres')  # noqa: E501

        # Validating name_ppgk_ipem
        if not is_num_characters_valid(name_ppkg_ipem, 10):
            self.errors_fields['name_ppkg_ipem'].append('O nome do setor de pré-embalados deve ter no mínimo 10 caracteres')  # noqa: E501

        # Validating size of images
        if img_uf and img_uf.size > (3 * 1024 * 1024):
            self.errors_fields['img_uf'].append('O tamanho da imagem do brasão do estado não pode ser maior que 3MB')  # noqa: E501
        if img_conv and img_conv.size > (3 * 1024 * 1024):
            self.errors_fields['img_conv'].append('O tamanho da imagem do convênio INMETRO/IPEM não pode ser maior que 3MB')  # noqa: E501

        if self.errors_fields:
            raise ValidationError(self.errors_fields)

        return super_clean
