import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from utils.exam_report import ExamReport


class HighErrorDispatchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors_fields = defaultdict(list)
        self.fields['dispatch_pdf'].widget.attrs.update({'multiple': True})

    dispatch_date = forms.DateField(
        required=True,
        label='Data do despacho',
        initial=dt.datetime.today().strftime('%Y-%m-%d'),
        widget=forms.DateInput(
            attrs={
                'class': 'form-file-input',
                'type': 'date',
            }
        )
    )

    dispatch_pdf = forms.FileField(
        label='Faça upload de um ou mais PDFs',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Só faça uploads de laudos de empresa com o mesmo CNPJ',
        required=True,
    )

    def clean(self):
        superclean = super().clean()
        obj_dt = self.cleaned_data.get('dispatch_date')
        dispatch_date = f'{obj_dt.day}/{obj_dt.month}/{obj_dt.year}'
        dispatch_pdf = self.files.getlist('dispatch_pdf')

        # Validating date
        valid_date = False
        masks = ['%d/%m/%y', '%d/%m/%Y']

        for mask in masks:
            try:
                dt.datetime.strptime(dispatch_date, mask)
                valid_date = True
            except ValueError:
                continue

        if not valid_date:
            self.errors_fields['dispatch_date'].append('A data informada é inválida')

        # Validating PDF files
        list_invalid_pdfs = []
        for pdf_file in dispatch_pdf:
            exam_report = ExamReport()
            valid_file = exam_report.loadRawData(pdf_file)
            if valid_file is False:
                list_invalid_pdfs.append(pdf_file.name)
        if len(list_invalid_pdfs) > 0:
            msg = f'Arquivo(s) inválido(s) encontrado(s): {', '.join(list_invalid_pdfs)}. '
            msg += 'Tente novamente sem esse(s) arquivo(s)'
            self.errors_fields['dispatch_pdf'].append(msg)

        if self.errors_fields:
            raise ValidationError(self.errors_fields)

        return superclean