import os

import pandas as pd
import pdfplumber as plb
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

def getExamReportObjectByType(pdf_file_object):
    """
    getExamReportObjectByType(filename)
    Returns a child object of ExamReport (ExamReportMass, ExamReportVol, etc.) given the name of a PDF object file.
    If the PDF object file isn't a valid exam report returns False
    """
    er = ExamReport()
    exam_report_valid = er.loadRawData(pdf_file_object)

    if exam_report_valid:
        type = er.getExamType()
        match type:
            case 'c':
                er = ExamReportLength()
                er.loadRawData(pdf_file_object)
                er.loadProdData()
            case 'u':
                er = ExamReportUnit()
                er.loadRawData(pdf_file_object)
                er.loadProdData()
            case 'm':
                er = ExamReportMass()
                er.loadRawData(pdf_file_object)
                er.loadProdData()
            case 'v':
                er = ExamReportVol()
                er.loadRawData(pdf_file_object)
                er.loadProdData()
        if er:
            return er
    else:
        return False

def extractScheduleToDictList(fileobj):
    pdf = plb.open(fileobj)
    lst_data = list()

    try:
        for page in pdf.pages:
            for table in page.extract_tables():
                data = [[x[0], x[5], x[3], x[6], x[7], x[8]] for x in table]
                lst_data.extend(data[1:])
    except Exception:
        return False

    df = pd.DataFrame(
        lst_data,
        columns=[
            'data',
            'tc',
            'produto',
            'marca',
            'qn',
            'quant'
        ]
    )

    return df.to_dict(orient='records')
