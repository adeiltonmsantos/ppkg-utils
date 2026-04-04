import json
import os

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from appDocuments.forms import IpemDataRegisterForm
from utils.appDocuments import get_imgs_path, get_ipem_data_json
from utils.django_midia import saveImageAsPng


class IpemData(View):
    def render_template(self, **kwargs):
        form = kwargs.get('form', None)
        form_data = kwargs.get('form_data', None)
        path_brasao = kwargs.get('path_brasao', None)
        path_convenio = kwargs.get('path_convenio', None)

        return render(
            self.request,
            'appDocuments/pages/ipem_data.html',
            context={
                'form': form,
                'form_data': form_data,
                'path_brasao': path_brasao,
                'path_convenio': path_convenio,
            }
        )

    def get(self, *args, **kwargs):
        # Getting data in ipem-data.json
        form_data = get_ipem_data_json()

        form = IpemDataRegisterForm(form_data)

        imgs_path = get_imgs_path()
        path_brasao = str(imgs_path['brasao'])
        path_convenio = str(imgs_path['convenio'])

        return self.render_template(
            form=form,
            path_brasao=path_brasao,
            path_convenio=path_convenio
        )

    def post(self, *args, **kwargs):
        files = self.request.FILES or None
        post = self.request.POST or None

        form = IpemDataRegisterForm(post, files)

        # Validation here
        if form.is_valid():
            # Content of JSON
            cleaned_data = form.cleaned_data
            form_data = {
                'uf_ipem': cleaned_data['uf_ipem'],
                'sec_ipem': cleaned_data['sec_ipem'],
                'rs_ipem': cleaned_data['rs_ipem'],
                'name_ppkg_ipem': cleaned_data['name_ppkg_ipem'],
            }

            # URL where JSON must be saved
            url_json = settings.BASE_DIR / 'appDocuments/ipem-data.json'

            # Trying to save JSON
            try:
                with open(url_json, 'w', encoding='UTF-8') as f:
                    json.dump(form_data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print('Erro encontrado: ', e)

            # Getting images as objects and inserting then in a list
            imgs = [
                {'name': 'brasao', 'file': self.request.FILES.get('img_uf', None)},  # noqa: E501
                {'name': 'convenio', 'file': self.request.FILES.get('img_conv', None)},  # noqa: E501
            ]

            for img in imgs:
                # Erasing previous files
                if os.path.exists(f"{settings.MEDIA_ROOT}/{img['name']}.png"):
                    os.remove(f"{settings.MEDIA_ROOT}/{img['name']}.png")

                # Saving new files, if sent
                if img['file'] is not None:
                    # Saving file as PNG
                    saveImageAsPng(img['file'], img['name'])

            imgs_path = get_imgs_path()
            path_brasao = str(imgs_path['brasao'])
            path_convenio = str(imgs_path['convenio'])
            form = IpemDataRegisterForm(form_data)

            messages.success(self.request, 'Dados salvos com sucesso!')

            return self.render_template(
                form=form,
                path_brasao=path_brasao,
                path_convenio=path_convenio
            )

        return redirect('appDocuments:ipem-data-send')
