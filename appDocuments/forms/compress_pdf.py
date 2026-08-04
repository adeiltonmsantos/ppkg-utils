
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class CompressPdfForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pdf_files'].widget.attrs.update({'multiple': True})

    pdf_files = forms.FileField(
        label='Selecione um ou mais arquivos PDFs',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        required=True,
        widget=forms.FileInput(attrs={'accept': 'application/pdf',})
    )

    def clean_pdf_files(self):
        pdf_cleaned = self.files.getlist('pdf_files')
        errors_list = []

        for pdf in pdf_cleaned:
            if pdf.size > 1024^2*25:
                errors_list.append(f'O arquivo {pdf.name} é maior que 25MB')

        if len(errors_list) > 0:
            raise ValidationError(errors_list)

        return pdf_cleaned