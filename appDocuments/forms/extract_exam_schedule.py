from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from utils.appDocuments import extractScheduleToDictList


class UploadExamSchedule(forms.Form):
    exam_schedule_pdf = forms.FileField(
        required=True,
        label='Cronograma de perícias',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    def clean(self):
        super().clean()
        file_schedule = self.files.get('exam_schedule_pdf')

        if file_schedule is not False:
            return extractScheduleToDictList(file_schedule)
        else:
            raise ValidationError('O arquivo enviado não é válido')

