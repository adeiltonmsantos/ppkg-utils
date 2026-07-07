from pathlib import Path
from unittest import TestCase

from django.conf import settings

from ..pdf_compress import PdfCompressor


class UnitTestCompressPDF(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.pdf_folder = Path(settings.BASE_DIR) / 'utils/tests/pdf_to_test_compress'
        return setup

    def test_several_pdf_to_compress(self):
        files_list = [pdffile for pdffile in self.pdf_folder.glob('*.pdf')]

        pdfcompressor = PdfCompressor()

        for pdf in files_list:
            file_str = str(pdf) 
            path_in = file_str
            path_out = file_str.replace('.pdf', 'comp.pdf')
            pdfcompressor.compress_pdf(path_in, path_out)
        
        compressed_list = [pdffile for pdffile in self.pdf_folder.glob('*comp.pdf')]

        self.assertEqual(
            len(files_list),
            len(compressed_list)
        )
    
    def test_compress_and_merge_pdfs(self):
        files_list = [pdffile for pdffile in self.pdf_folder.glob('*.pdf')]

        pdfcompressor = PdfCompressor()
        pdfcompressor.compress_and_merge(files_list, 'MERGEDFILES')

        merged_files = [pdffile for pdffile in self.pdf_folder.glob('*MERGEDFILES*.pdf')]

        self.assertGreater(len(merged_files), 0)
