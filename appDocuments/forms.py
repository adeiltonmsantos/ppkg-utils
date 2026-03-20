from django import forms
from django.core.exceptions import ValidationError


def add_error_message_to_field(field, error_type, error_message):
    field.error_messages[error_type] = error_message


def validate_file_size(value):
    filesize = value.size
    # 3MB em bytes
    if filesize > 3 * 1024 * 1024:
        raise ValidationError("A imagem não pode ser maior que 3MB.")
    return value


def validate_uf_field(value):
    if value == ' ':
        raise ValidationError('Selecione um estado')


def validate_size_characters(num_chars, field_label):
    def effective_validator(value):
        if len(str(value).strip()) < num_chars:
            raise ValidationError(
                f'O campo "{field_label}" não pode ter menos de {num_chars} caracteres')  # noqa: E501


class IpemDataRegisterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        validators=[validate_uf_field]
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
        validators=[validate_file_size]
    )

    img_conv = forms.FileField(
        required=False,
        label='Imagem do convênio INMETRO/IPEM',
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'accept': 'image/*'
        }),
        validators=[validate_file_size]
    )
