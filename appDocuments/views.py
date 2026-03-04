import json
import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import (
    redirect,
    render,  # noqa: F401
)

# from django.urls import reverse
from .forms import IpemDataRegisterForm


def home(request):
    ...


def ipemData_receive(request):
    if not request.POST:
        raise Http404()

    files = request.FILES
    post = request.POST
    request.session['register_form_data'] = post
    form = IpemDataRegisterForm(request.session['register_form_data'], files)

    # Validação aqui
    if form.is_valid():
        # Conteúdo do JSON
        cleaned_data = form.cleaned_data
        content = {
            'uf': cleaned_data['uf_ipem'],
            'sec_ipem': cleaned_data['sec_ipem'],
            'rs_ipem': cleaned_data['rs_ipem'],
            'name_ppkg_ipem': cleaned_data['name_ppkg_ipem'],
        }

        # Salvando o JSON na pasta do app
        url_json = settings.BASE_DIR / 'appDocuments'

        # Tentando salvar o JSON
        try:
            with open(url_json, 'w', encoding='UTF-8') as f:
                json.dump(content, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    # Validação falhou. Renderizando novamente
    return redirect('appDocuments:ipem-data-send')


def ipemData_send(request):
    register_form_data = request.session.get('register_form_data', None)
    files = request.FILES or None
    form = IpemDataRegisterForm(register_form_data, files)
    return render(request,
                  'appDocuments/pages/ipem_data.html',
                  context={'form': form}
                  )
