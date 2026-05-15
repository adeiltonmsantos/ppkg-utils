from unittest import TestCase

from parameterized import parameterized

from utils.appDocuments import getExamReportObjectByType, loadExamReportPDF
from utils.exam_report import (
    ExamReport,
)


class UnitTestExamReport(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.exam_rep = ExamReport()
        # self.pdf_folder = Path(__file__).parent / 'reports_to_test'
        return setup
    
    def test_if_file_is_a_valid_pdf_exam_report(self):
        # Exam Report Object
        er = self.exam_rep

        # Exam report path to test
        pdf_name = 'ld_mass_rp_01.pdf'

        # Loading to memory a PDF file to test
        pdf_file = loadExamReportPDF(pdf_name)

        # Testing if the file is a PDF
        data = er.loadRawData(pdf_file)
        valid_file = data is not False

        # Testing a valid exam report
        self.assertTrue(
            valid_file,
            msg="File doesn't exist or is not a PDF file"
        )

        # File wich is not a exam report
        pdf_name = 'ld_invalid.pdf'
        pdf_file = loadExamReportPDF(pdf_name)
        data = er.loadRawData(pdf_file)

        # Testing an invalid exam report
        self.assertFalse(
            data
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
        pdf_file = loadExamReportPDF(filename)

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
        er = getExamReportObjectByType(filename)
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
        er = getExamReportObjectByType(filename)
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
        er = getExamReportObjectByType(filename)
        self.assertTrue(er.isSubjectToDispatch())