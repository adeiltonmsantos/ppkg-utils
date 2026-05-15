import io
import os
from pathlib import Path

from django.conf import settings

from utils.exam_report import (
    ExamReport,
    ExamReportLength,
    ExamReportMass,
    ExamReportUnit,
    ExamReportVol,
)


def get_imgs_path():
    # Verifying if images exist
    imgs = ['brasao', 'convenio', 'assinatura']
    imgs_path = {}

    for img in imgs:
        try:
            if os.path.exists(settings.MEDIA_ROOT + f'{img}.png'):
                imgs_path[img] = settings.MEDIA_ROOT + f'{img}.png'
            else:
                imgs_path[img] = None
        except Exception:
            if os.path.exists(settings.MEDIA_ROOT / f'{img}.png'):
                imgs_path[img] = settings.MEDIA_ROOT / f'{img}.png'
            else:
                imgs_path[img] = None

    return imgs_path

def loadExamReportPDF(pdf_name):
    # Exam report path to test
    pdf_folder = Path(__file__).parent / 'tests/reports_to_test'
    pdf_path = pdf_folder / pdf_name

    # Trying to load to memory a PDF file to test
    try:
        with open(pdf_path, 'rb') as f:
            pdf_file = io.BytesIO(f.read())
            return pdf_file
    except Exception:
        return False

def getExamReportObjectByType(filename):
    # Loading to memory a PDF file to test
    pdf_file = loadExamReportPDF(filename)
    er = ExamReport()
    er.loadRawData(pdf_file)
    type = er.getExamType()
    match type:
        case 'c':
            er = ExamReportLength()
            er.loadRawData(pdf_file)
            er.loadProdData()
        case 'u':
            er = ExamReportUnit()
            er.loadRawData(pdf_file)
            er.loadProdData()
        case 'm':
            er = ExamReportMass()
            er.loadRawData(pdf_file)
            er.loadProdData()
        case 'v':
            er = ExamReportVol()
            er.loadRawData(pdf_file)
            er.loadProdData()
    if er:
        return er
