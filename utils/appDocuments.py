import os

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