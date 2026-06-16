from django import forms
from django.core.exceptions import ValidationError

from utils.appDocuments import extractScheduleToDictList


class UploadExamScheduleForm(forms.Form):
    exam_schedule_pdf = forms.FileField(
        required=True,
        label='Cronograma de perícias',
        widget=forms.FileInput(
            attrs={'accept': 'application/pdf',}
        )
    )

    def clean_exam_schedule_pdf(self):
        super().clean()
        file_schedule = self.files.get('exam_schedule_pdf')
        result = extractScheduleToDictList(file_schedule)

        if result is not False:
            return result
        else:
            raise ValidationError('O arquivo enviado não é válido')

class EditExamScheduleForm(forms.Form):
    exam_schedule_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    # def clean_exam_schedule_data(self):
    #     ...