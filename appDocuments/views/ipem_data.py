import json
import os
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView

from appDocuments.forms import IpemDataRegisterForm
from utils.appDocuments import get_imgs_path
from utils.django_midia import saveImageAsPng

JSON_PATH = Path(apps.get_app_config('appDocuments').path) / 'ipem-data.json'


class HomeView(TemplateView):
    template_name = 'global/pages/base.html'


class IpemData(View):

    def render_template(self, **kwargs):
        form = kwargs.get('form', None)
        form_data = kwargs.get('form_data', None),
        path_brasao = kwargs.get('path_brasao', None)
        path_convenio = kwargs.get('path_convenio', None)

        return render(
            self.request,
            'appDocuments/pages/ipem_data.html',
            context={
                'form': form,
                'form_data': form_data,
                'title_form': 'DADOS CADASTRAIS DO IPEM',
                'path_brasao': path_brasao,
                'path_convenio': path_convenio,
            }
        )

    def get(self, *args, **kwargs):
        # Getting data in ipem-data.json
        json_path = JSON_PATH
        with open(json_path, 'r', encoding='utf-8') as file:
            form_data = json.load(file)

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
        else:
            imgs_path = get_imgs_path()
            path_brasao = str(imgs_path['brasao'])
            path_convenio = str(imgs_path['convenio'])

            return self.render_template(
                form=form,
                form_data=self.request.POST,
                path_brasao=path_brasao,
                path_convenio=path_convenio,
            )

        return redirect('appDocuments:ipem-data-send')
