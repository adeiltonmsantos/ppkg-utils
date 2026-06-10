import json

from django.shortcuts import render
from django.views.generic import FormView

from appDocuments.forms import EditExamScheduleForm, UploadExamScheduleForm
from utils.appDocuments import extractScheduleToDictList


class UploadExamSchedule(FormView):
    template_name = 'appDocuments/pages/upload_exam_schedule.html'
    form_class = UploadExamScheduleForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_form'] = 'Upload de Cronograma de Perícias'
        return context
    
    def form_valid(self, form):
        pdf_file = self.request.FILES['exam_schedule_pdf']
        data = json.dumps(extractScheduleToDictList(pdf_file), ensure_ascii=False)

        return render(
            self.request,
            'appDocuments/pages/edit_uploaded_exam_schedule.html',
            {data: data}
        )

class EditExamSchedule(FormView):
    template_name = 'appDocuments/pages/edit_uploaded_exam_schedule.html'
    form_class = EditExamScheduleForm
    success_url = reversed('appDocuments:edit-exam-schedule')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_form'] = 'Validação de Cronograma de Perícias'
        return context

