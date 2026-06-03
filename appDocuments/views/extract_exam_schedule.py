from django.urls import reverse_lazy
from django.views.generic import FormView

from appDocuments.forms import ExtractExamSchedule


class UploadExamSchedule(FormView):
    template_name = 'appDocuments/extract_exam_schedule.html'
    form_class = ExtractExamSchedule
    success_url = reverse_lazy('')