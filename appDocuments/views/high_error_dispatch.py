from django.shortcuts import render
from django.views import View

from appDocuments.forms.high_error_dispatch import HighErrorDispatchForm
from utils.exam_report import ExamReport


class HighErrorDispatch(View):
    def render_template(self, **kwargs):
        form = kwargs.get('form', None)
        form_data = kwargs.get('form_data', None),

        return render(
            self.request,
            'appDocuments/pages/high_error_dispatch.html',
            context={
                'form': form,
                'form_data': form_data,
                'title_form': 'DESPACHO PARA ERROS ELEVADOS',
            }
        )
    
    def get(self, *args, **kwargs):
        form = HighErrorDispatchForm()
        return self.render_template(form=form)
    
    def post(self, *args, **kwargs):
        data = self.request.POST or None
        files = self.request.FILES.getlist('dispatch_pdf') or None
        form = HighErrorDispatchForm(data=data, files=files)

        if form.is_valid():
            dispatch_date = form.cleaned_data.get('dispatch_date')
            dispatch_pdf = form.files.get('dispatch_pdf')

            # Routine to generate dispatch here
            report = ExamReport()
            for f in dispatch_pdf:
                rp = report.loadRawData(f)

                pass
        else:
            return self.render_template(
                form=form,
            )