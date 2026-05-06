import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError


class HighErrorDispatchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors_fields = defaultdict(list)

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
        required=True,
        label='Faça upload de um ou mais PDFs',
        widget=forms.FileInput(
            attrs={
                'class': 'form-file-input',
                'accept': 'application/pdf'
            }
        ),
    )

    def clean(self):
        superclean = super().clean()
        dispatch_date = self.cleaned_data.get('dispatch_date')
        dispatch_pdf = self.files.get('dispatch_pdf')

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

        if self.errors_fields:
            raise ValidationError(self.errors_fields)

        return superclean