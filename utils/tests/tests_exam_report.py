import io
from pathlib import Path
from unittest import TestCase

from parameterized import parameterized

from utils.appDocuments import getExamReportObjectByType
from utils.exam_report import ExamReport


class UnitTestExamReport(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.exam_rep = ExamReport()
        self.pdf_folder = Path(__file__).parent / 'reports_to_test'
        return setup
    
    def loadExamReportPDF(self, pdf_name):
        """
        loadExamReportPDF(pdf_name)
        Returns a PDF file object in memory based on the name of a PDF in utils/tests/reports_to_test.
        If file doesn't exist returns False
        """
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

        # Loading to memory a valid PDF file to test
        pdf_name = 'ld_mass_rp_01.pdf'
        pdf_file = self.loadExamReportPDF(pdf_name)

        # Testing a valid exam report
        self.assertTrue(
            er.loadRawData(pdf_file),
            msg="File doesn't exist or is not a PDF file"
        )

        # Loading to memory an invalid PDF file to test
        pdf_name = 'ld_invalid.pdf'
        pdf_file = self.loadExamReportPDF(pdf_name)

        # Testing an invalid exam report
        self.assertFalse(
            er.loadRawData(pdf_file)
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

    @parameterized.expand([
        ('ld_high_rp_01.pdf', 'c'),
        ('ld_length_rp_01.pdf', 'c'),
        ('ld_width_rp_01.pdf', 'c'),
        ('ld_unid_ap_01.pdf', 'u'),
        ('ld_mass_rp_01.pdf', 'm'),
        ('ld_vol_rp_01.pdf', 'v'),
        # ('ld_invalid.pdf', 'v'),
    ])
    def test_if_returns_number_of_errors(self, filename, type):
        pdf_obj = self.loadExamReportPDF(filename)
        er = getExamReportObjectByType(pdf_obj)
        self.assertIsNotNone(er.perc_defective)

    @parameterized.expand([
        ('ld_high_rp_01.pdf', 'c'),
        ('ld_length_rp_01.pdf', 'c'),
        ('ld_width_rp_01.pdf', 'c'),
        ('ld_unid_ap_01.pdf', 'u'),
        ('ld_mass_rp_01.pdf', 'm'),
        ('ld_vol_rp_01.pdf', 'v'),
        # ('ld_invalid.pdf', 'v'),
    ])
    def test_percentage_of_errors(self, filename, type):
        pdf_obj = self.loadExamReportPDF(filename)
        er = getExamReportObjectByType(pdf_obj)
        self.assertIsNotNone(er.perc_defective)

    @parameterized.expand([
        ('ld_high_rp_01.pdf'),
        ('ld_length_rp_01.pdf'),
        ('ld_width_rp_01.pdf'),
        # ('ld_unid_ap_01.pdf'),
        ('ld_mass_rp_01.pdf'),
        ('ld_vol_rp_01.pdf'),
        # ('ld_invalid.pdf'),
    ])
    def test_if_exam_report_is_subject_to_dispatch(self, filename):
        pdf_obj = self.loadExamReportPDF(filename)
        er = getExamReportObjectByType(pdf_obj)
        self.assertTrue(er.isSubjectToDispatch())