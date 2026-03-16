import io
import json
from pathlib import Path

from django.conf import settings

# import os
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import (
    redirect,
    render,  # noqa: F401
)
from PIL import Image

# from django.urls import reverse
from .forms import IpemDataRegisterForm


def home(request):
    ...


def ipemData_receive(request):
    def changeExtensionImage(ImgObj):
        # Extraindo nomes e extensões dos arquivos
        ImgObj_aux = Path(ImgObj.name)
        ImgObj_ext = ImgObj_aux.suffix.lower()

        if ImgObj_ext != '.png':
            img = Image.open(ImgObj)
            buffer = io.BytesIO()
            ImgObj = img.save(buffer, format='PNG')

        return ImgObj

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
        url_json = settings.BASE_DIR / 'appDocuments/ipem-data.json'

        # Tentando salvar o JSON
        try:
            with open(url_json, 'w', encoding='UTF-8') as f:
                json.dump(content, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print('Erro encontrado: ', e)

        # Obtendo as imagens como objetos em PNG
        brasao = changeExtensionImage(request.FILES['img_uf'])
        convenio = changeExtensionImage(request.FILES['img_conv'])

        fs = FileSystemStorage()

        # Lista com nomes das imagens
        imgs = ['brasao.png', 'convenio.png']

        for img in imgs:
            # Apagando arquivos pré-existentes
            if fs.exists(img):
                fs.delete(img)

        # Salvando imagens na pasta 'media'
        fs.save('brasao.png', brasao)
        fs.save('convenio.png', convenio)

        form = IpemDataRegisterForm()
        return render(
            request,
            'appDocuments/pages/ipem_data.html',
            context={'form': form}
        )

    return redirect('appDocuments:ipem-data-send')


def ipemData_send(request):
    register_form_data = request.session.get('register_form_data', None)
    files = request.FILES or None
    form = IpemDataRegisterForm(register_form_data, files)
    return render(request,
                  'appDocuments/pages/ipem_data.html',
                  context={'form': form}
                  )
