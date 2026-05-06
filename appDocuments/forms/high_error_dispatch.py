import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError


# Overwriting ClearableFileInput
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# Creating field to accept multile files upload
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
    
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

    dispatch_pdf = MultipleFileField(
        widget=MultipleFileInput(
            attrs={
                'multiple': True,
                'class': 'form-file-input',
                'accept': 'application/pdf',
            }
        ),
        required=True,
        label='Faça upload de um ou mais PDFs',
    )

    def clean(self):
        superclean = super().clean()
        obj_dt = self.cleaned_data.get('dispatch_date')
        dispatch_date = f'{obj_dt.day}/{obj_dt.month}/{obj_dt.year}'
        # dispatch_pdf = self.files.get('dispatch_pdf')

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