from django.shortcuts import render
from django.views import View


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
        return self.render_template()