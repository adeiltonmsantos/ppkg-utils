import io
from pathlib import Path
from unittest import TestCase

from parameterized import parameterized

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


    def test_if_file_is_a_valid_pdf_exam_report(self):
        # Exam Report Object
        er = self.exam_rep

        # Exam report path to test
        pdf_name = 'ld_mass_rp_01.pdf'

        # Loading to memory a PDF file to test
        pdf_file = self.loadExamReportPDF(pdf_name)

        # Testing if the file is a PDF
        er.loadRawData(pdf_file)
        self.assertIn(
            'SERVIÇO PÚBLICO FEDERAL',
            er.list_raw_data[0][0],
            msg="File doesn't exist or is not a PDF file"
        )

    @parameterized.expand([
        ('ld_high_rp_01.pdf', 'c'),
        ('ld_length_rp_01.pdf', 'c'),
        ('ld_width_rp_01.pdf', 'c'),
        ('ld_unid_ap_01.pdf', 'u'),
        ('ld_mass_rp_01.pdf', 'm'),
        ('ld_vol_rp_01.pdf', 'v'),
    ])
    def test_if_returns_type_of_report_exam_correctly(self, filename, type_exam):
        # Loading to memory a PDF file to test
        pdf_file = self.loadExamReportPDF(filename)

        self.exam_rep.loadRawData(pdf_file)
        exam_type = self.exam_rep.getExamType()
        self.assertIs(exam_type,
                      type_exam,
                      msg="File doesn't exist or is invalid"
        )


