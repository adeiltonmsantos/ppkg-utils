from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views import View

from appDocuments.forms.high_error_dispatch import HighErrorDispatchForm
from utils.appDocuments import getExamReportObjectByType
from utils.dispatch import Dispatch

DISPATCH_FOLDER = settings.DISPATCH_PATH or None

class HighErrorDispatch(View):
    def render_template(self, **kwargs):
        form = kwargs.get('form', None)
        form_data = kwargs.get('form_data', None),
        dispatch_url = kwargs.get('dispatch_url', None)

        return render(
            self.request,
            'appDocuments/pages/high_error_dispatch.html',
            context={
                'form': form,
                'form_data': form_data,
                'title_form': 'DESPACHO PARA ERROS ELEVADOS',
                'dispatch_url': dispatch_url,
            }
        )
    
    def get(self, *args, **kwargs):
        form = HighErrorDispatchForm()
        return self.render_template(form=form)
    
    def post(self, *args, **kwargs):
        data = self.request.POST or None
        files = self.request.FILES or None
        form = HighErrorDispatchForm(data=data, files=files)

        if form.is_valid():
            dispatch_date = form.cleaned_data['dispatch_date'].strftime('%d/%m/%Y')
            dispatch_pdf = form.files.getlist('dispatch_pdf')
            errors = []

            # Routine to generate dispatch here
            for f in dispatch_pdf:
                er = getExamReportObjectByType(f)
                if er.isSubjectToDispatch():
                    errors.append(er.getErrosTxt())

            url = None
            if len(errors) > 0:
                dp = Dispatch(errors, dispatch_date=dispatch_date)
                url = dp.makeDispatchPDF(pathfile=DISPATCH_FOLDER, perc_w_signature=80)
            else:
                messages.info(self.request, 'Não há erros para geração de despacho no(s) arquivo(s) enviado(s)')

            return self.render_template(form=form, dispatch_url=url)
        else:
            return self.render_template(
                form=form,
            )