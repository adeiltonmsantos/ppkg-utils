import io
from pathlib import Path
from unittest import TestCase

from utils.exam_report import ExamReport


class UnitTestExamReport(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.exam_rep = ExamReport()
        self.pdf_folder = Path(__file__).parent / 'reports_to_test'
        return setup
    
    def loadExamReportPDF(self, pdf_name):
        # Exam report path to test
        pdf_path = self.pdf_folder / pdf_name

        # Trying to load to memory a PDF file to test
        try:
            with open(pdf_path, 'rb') as f:
                pdf_file = io.BytesIO(f.read())
                return pdf_file
        except Exception:
            return False


    def test_if_pdf_is_a_valid_exam_report(self):
        # Exam Report Object
        er = self.exam_rep

        # Exam report path to test
        pdf_name = 'ld_mass_02.pdf'

        # Loading to memory a PDF file to test
        pdf_file = self.loadExamReportPDF(pdf_name)

        # Testing if the file is a PDF
        if pdf_file:
            # Loading data from PDF file
            result = er.loadRawData(pdf_file)

            if result:
                self.assertIn(
                    'SERVIÇO PÚBLICO FEDERAL',
                    er.list_raw_data[0][0]
                )

