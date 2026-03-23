# import io
import json

# from pathlib import Path
from django.conf import settings
from django.contrib import messages

# import os
# from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import (
    redirect,
    render,  # noqa: F401
)

# from PIL import Image
from utils.django_midia import saveImageAsPng

# from django.urls import reverse
from .forms import IpemDataRegisterForm


def home(request):
    ...


def ipemData_receive(request):
    # def saveImageAsPng(ImgObj, ImgName):
    #     # Extraindo nomes e extensões dos arquivos
    #     ImgObj_aux = Path(ImgObj.name)
    #     ImgObj_ext = ImgObj_aux.suffix.lower()

    #     # Arquivo não é PNG. Convertendo e inserindo o conteúdo no buffer...
    #     if ImgObj_ext != '.png':
    #         img = Image.open(ImgObj)
    #         # Criando um buffer para armazenar o arquivo em memória
    #         buffer = io.BytesIO()
    #         img.save(buffer, format='PNG')
    #         img_content = ContentFile(buffer.getvalue())

    #     # Arquivo é PNG. Gerando apenas o conteúdo para inserir no buffer...
    #     else:
    #         img_content = ImgObj
    #     img_name = f'{ImgName}.png'

    #     # Salvando o arquivo...
    #     fs = FileSystemStorage()
    #     fs.save(img_name, img_content)

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

        fs = FileSystemStorage()

        for img in imgs:
            # Apagando arquivos pré-existentes
            if fs.exists(f"{img['name']}.png"):
                fs.delete(f"{img['name']}.png")

            # Salvando novos arquivos, se foram enviados
            if img['file'] is not None:
                # Salvando arquivo como PNG
                saveImageAsPng(img['file'], img['name'])

        form = IpemDataRegisterForm()

        messages.success(request, 'Dados salvos com sucesso!')

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
