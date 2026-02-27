from django import forms


def add_error_message_to_field(field, error_type, error_message):
    field.error_messages[error_type] = error_message


class IpemDataRegisterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    uf_ipem = forms.CharField(
        label='Estado do IPEM',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Alagoas, Bahia, Ceará, ...',
            'class': 'form-text-input'
        }),
        error_messages={
            'required': 'O campo "Estado do IPEM" é obrigatório'
        }
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
        required=True,
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
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Divisão de Pré-Embalados',
            'class': 'form-text-input'
        }),
        error_messages={
            'required': 'A "Nome" do setor de Pré-Embalados é obrigatório'
        }
    )

    img_uf = forms.FileField(
        label='Imagem do brasão do estado',
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'accept': 'image/*'
        })
    )

    img_conv = forms.FileField(
        label='Imagem do convênio INMETRO/IPEM',
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'accept': 'image/*'
        })
    )
