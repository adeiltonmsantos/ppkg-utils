import io
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from PIL import Image


def saveImageAsPng(ImgObj, ImgName):
    """
    saveImagePng(ImgObj, ImgName)
    Saves an image as a PNG in MEDIA_ROOT regardless of its original format:
    - ImgObj: image file object
    - Imgname: name of the image (without extension)
    """
    # Extraindo nomes e extensões dos arquivos
    ImgObj_aux = Path(ImgObj.name)
    ImgObj_ext = ImgObj_aux.suffix.lower()

    # Arquivo não é PNG. Convertendo e inserindo o conteúdo no buffer...
    if ImgObj_ext != '.png':
        img = Image.open(ImgObj)
        # Criando um buffer para armazenar o arquivo em memória
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_content = ContentFile(buffer.getvalue())

    # Arquivo é PNG. Gerando apenas o conteúdo para inserir no buffer...
    else:
        img_content = ImgObj
    img_name = f'{ImgName}.png'

    # Salvando o arquivo...
    fs = FileSystemStorage()
    fs.save(img_name, img_content)
