from django import forms


def add_error_message_to_field(field, error_type, error_message):
    field.error_messages[error_type] = error_message


class IpemDataRegisterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_error_message_to_field(
            self.fields['uf_ipem'],
            'required',
            'O "Estado" do IPEM é obrigatório'
        )

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
            'required': 'O campo "Estado do IPEM" é obrigatório'
        }
    )

    name_ipem = forms.CharField(
        label='Nome do IPEM',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Inst. de Metrologia e Qualidade de Alagoas',
            'class': 'form-text-input'
        })
    )

    name_ppkg_ipem = forms.CharField(
        label='Nome do setor de Pré-Embalados',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Divisão de Pré-Embalados',
            'class': 'form-text-input'
        })
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
