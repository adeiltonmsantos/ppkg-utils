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

    def test_if_several_pdfs_compressed_are_returned_as_a_list(self):
        # List with PDF files in folder for tests
        files_list = [pdffile.read_bytes() for pdffile in self.pdf_folder.glob('*.pdf')]

        pdfcomp = PdfCompressor()

        compressed_list = pdfcomp.compress_several_pdfs(files_list)

        # pathpdf = self.pdf_folder
        # for i, file in enumerate(compressed_list):
        #     i += 1
        #     (pathpdf / f'EMBALAGEM-{i}.pdf').write_bytes(file)

        # Total files sizes before compressing
        total_before = sum([len(f) for f in files_list])

        # Total files list after compressing
        total_after = sum([len(f) for f in compressed_list])

        self.assertTrue(
            total_after <= total_before
        )

    def test_merge_files(self):
        # List with PDF files
        files = [pdffile.read_bytes() for pdffile in self.pdf_folder.glob('*.pdf')]

        # Merging files...
        pdfcompressor = PdfCompressor()
        mergedfiles = pdfcompressor.merge_several_pdfs(files_list=files)

        # Total size of files before merging...
        size_before = sum([len(f) for f in files])

        # Total size after merging...
        size_after = len(mergedfiles)

        self.assertTrue(size_after <= size_before)
    
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
        