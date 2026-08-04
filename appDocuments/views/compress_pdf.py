from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from ..forms import CompressPdfForm


class CompressPdfView(FormView):
    template_name = ''
    form_class = CompressPdfForm
    success_url = reverse_lazy(template_name)