import json
import os

# from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import (
    redirect,
    render,
)

from utils.appDocuments import get_imgs_path, get_ipem_data_json
from utils.django_midia import saveImageAsPng

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
            'uf_ipem': cleaned_data['uf_ipem'],
            'sec_ipem': cleaned_data['sec_ipem'],
            'rs_ipem': cleaned_data['rs_ipem'],
            'name_ppkg_ipem': cleaned_data['name_ppkg_ipem'],
        }

        # URL onde o JSON deve ser salvo
        url_json = settings.BASE_DIR / 'appDocuments/ipem-data.json'

        # Tentando salvar o JSON
        try:
            with open(url_json, 'w', encoding='UTF-8') as f:
                json.dump(content, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print('Erro encontrado: ', e)

        # Obtendo as imagens como objetos e inserindo em lista
        imgs = [
            {'name': 'brasao', 'file': request.FILES.get('img_uf', None)},
            {'name': 'convenio', 'file': request.FILES.get('img_conv', None)},
        ]

        # fs = FileSystemStorage()

        for img in imgs:
            # Apagando arquivos pré-existentes
            if os.path.exists(f"{settings.MEDIA_ROOT}/{img['name']}.png"):
                os.remove(f"{settings.MEDIA_ROOT}/{img['name']}.png")

            # Salvando novos arquivos, se foram enviados
            if img['file'] is not None:
                # Salvando arquivo como PNG
                saveImageAsPng(img['file'], img['name'])

        imgs_path = get_imgs_path()
        path_brasao = str(imgs_path['brasao'])
        path_convenio = str(imgs_path['convenio'])
        form = IpemDataRegisterForm(content)

        messages.success(request, 'Dados salvos com sucesso!')

        return render(
            request,
            'appDocuments/pages/ipem_data.html',
            context={
                'form': form,
                'path_brasao': path_brasao,
                'path_convenio': path_convenio,
            }
        )

    return redirect('appDocuments:ipem-data-send')


def ipemData_send(request):
    # Getting data in ipem-data.json
    form_data = get_ipem_data_json()

    form = IpemDataRegisterForm(form_data)

    imgs_path = get_imgs_path()
    path_brasao = str(imgs_path['brasao'])
    path_convenio = str(imgs_path['convenio'])

    return render(request,
                  'appDocuments/pages/ipem_data.html',
                  context={
                      'form': form,
                      'form_data': form_data,
                      'path_brasao': path_brasao,
                      'path_convenio': path_convenio,
                      }
                  )
