from django.urls import reverse_lazy
from django.views.generic import FormView

from appDocuments.forms import UploadExamSchedule


class UploadExamSchedule(FormView):
    template_name = 'appDocuments/upload_exam_schedule.html'
    form_class = UploadExamSchedule
    success_url = reverse_lazy('')