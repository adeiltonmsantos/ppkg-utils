import io
from pathlib import Path
from unittest import TestCase

from parameterized import parameterized

from utils.exam_report import (
    ExamReport,
)


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
        er = self.exam_rep
        pdf_obj = self.loadExamReportPDF('ld_mass_rp_01.pdf')
        result = er.loadRawData(pdf_obj)

        # Testing a valid exam report
        self.assertTrue(
            result is not False,
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
        ('ld_high_rp_01.pdf'),
        ('ld_length_rp_01.pdf'),
        ('ld_width_rp_01.pdf'),
        ('ld_mass_rp_01.pdf'),
        ('ld_vol_rp_01.pdf'),
        ('ld04.pdf'),
    ])
    def test_if_exam_report_is_subject_to_dispatch(self, filename):
        pdf_obj = self.loadExamReportPDF(filename)
        er = self.exam_rep
        er.loadRawData(pdf_obj)
        self.assertTrue(
            er.isSubjectToDispatch(),
            msg=f'File "{filename}" is not subject to dispatch'
        )

    @parameterized.expand([
        ('ld_high_rp_01.pdf'),
        ('ld_length_rp_01.pdf'),
        ('ld_width_rp_01.pdf'),
        ('ld_mass_rp_01.pdf'),
        ('ld_vol_rp_01.pdf'),
        ('ld04.pdf'),
    ])
    def test_if_loads_whole_relevant_data_of_product_and_exam(self, pdfname):
        er = self.exam_rep
        pdf_obj = self.loadExamReportPDF(pdfname)
        er.loadRawData(pdf_obj)

        # Testing exam report type
        exam_type = er.exam_report_type
        self.assertFalse(str(exam_type) == 'None' or str(exam_type) == '')

        # Testing product name
        prod_name = er.product_name
        self.assertFalse(str(prod_name) == 'None' or str(prod_name) == '')

        # Testing product brand
        prod_brand = er.product_brand
        self.assertFalse(str(prod_brand) == 'None' or str(prod_brand) == '')

        # Testing nominal product content
        qn_product = er.qn_product
        self.assertFalse(str(qn_product) == 'None' or str(qn_product) == '')

        # Testing sample size
        n = er.n
        self.assertFalse(str(n) == 'None' or str(n) == '')

        # Testing unit product
        unit_product = er.unit_product
        self.assertFalse(str(unit_product) == 'None' or str(unit_product) == '')

        # Testing total number of sample units with individual error
        total_error = er.total_defective
        self.assertFalse(str(total_error) == 'None' or str(total_error) == '')

        # Testing Qn - T
        min_ind_value = er.min_individual_value
        self.assertFalse(str(min_ind_value) == 'None' or str(min_ind_value) == '')

        # Testing percentual of defective units
        perc_def = er.perc_defective
        self.assertFalse(str(perc_def) == 'None' or str(perc_def) == '')

        # Testing T3 value
        T3 = er.T3
        self.assertFalse(str(T3) == 'None' or str(T3) == '')

        # Testing T3 error value (Qn - 3T) 
        T3_value = er.T3_error_value
        self.assertFalse(str(T3_value) == 'None' or str(T3_value) == '')

        # Testing exam values list
        data = er.measurements_list
        self.assertTrue(len(data) >= 5)



