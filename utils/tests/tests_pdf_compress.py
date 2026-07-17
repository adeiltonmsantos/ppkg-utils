from pathlib import Path
from unittest import TestCase

from django.conf import settings

from ..pdf_compress import PdfCompressor


class UnitTestCompressPDF(TestCase):
    def setUp(self):
        setup = super().setUp()
        self.pdf_folder = Path(settings.BASE_DIR) / 'utils/tests/pdf_to_test_compress'
        return setup

    def test_a_single_pdf_to_compress(self):
        # loading a file from test folder
        files_list = [(file.stem, file) for file in self.pdf_folder.iterdir() if file.is_file()]
        pdf_name = files_list[0][0]
        pdf_obj = (self.pdf_folder / f'{pdf_name}.pdf').read_bytes()
        
        # PdfCompressor object
        pdf_comp = PdfCompressor()

        # Compressing PDF file
        compressed = pdf_comp.compress_pdf(pdf_obj)

        pdf_obj = self.pdf_folder / f'{pdf_name}_comp.pdf'
        pdf_obj.write_bytes(compressed)

    def test_several_pdf_to_compress_individually(self):
        files_list = [(pdffile.read_bytes(), pdffile.stem) for pdffile in self.pdf_folder.glob('*.pdf')]

        pdfcompressor = PdfCompressor()

        for pdf in files_list:
            pdf_bytes = pdfcompressor.compress_pdf(pdf[0])
            path_obj = self.pdf_folder / f'{pdf[1]}-compress.pdf'
            path_obj.write_bytes(pdf_bytes)
        
        compressed_list = [pdffile for pdffile in self.pdf_folder.glob('*compress.pdf')]

        self.assertEqual(
            len(files_list),
            len(compressed_list)
        )
    
    def test_compress_and_merge_several_pdfs(self):
        # Defining list with bytes of PDF files in disc
        files_list = [pdffile.read_bytes() for pdffile in self.pdf_folder.glob('*.pdf')]

        # Compressing and meging files
        pdfcompressor = PdfCompressor()
        pdfmerged = pdfcompressor.compress_and_merge(files_list)

        # Testing if the compressed and merged file is not empty
        self.assertTrue(
            len(pdfmerged) > 0,
            msg='Result of operation is an empty file'
        )

        # Testing if the compressed and merged file is a valid PDF
        self.assertTrue(
            pdfmerged.startswith(b"%PDF"),
            msg='Result of operation is not a valid PDF file'
        )
        