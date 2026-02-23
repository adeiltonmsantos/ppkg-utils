from django import forms


class IpemDataRegisterForm(forms.Form):
    uf_ipem = forms.CharField(
        label='Estado do IPEM',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Alagoas, Bahia, Ceará, ...',
            'class': 'form-text-input'
        })
    )

    sec_ipem = forms.CharField(
        label='Secretaria de Estado ao qual o IPEM é vinculado',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Secretaria de Estado de Ind. e Comércio',
            'class': 'form-text-input'
        })
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
        label='Imagem do brasão do estado'
    )

    img_conv = forms.FileField(
        label='Imagem do convênio INMETRO/IPEM'
    )
