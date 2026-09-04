import io
import os
import subprocess
import tempfile

from pypdf import PdfWriter


class PdfCompressor:
    """
    PdfCompressor
    -------------
    A class that can compress PDF files and merge them into a single file.
    """

    def __init__(self, limit_MB_file=20):
        self.limit_MB_file = limit_MB_file

    def _extract_bytes(self, pdf_object):
        """
        Auxiliary method for extracting bytes from any type of PDF object
        """
        if isinstance(pdf_object, bytes):
            return pdf_object
        
        if hasattr(pdf_object, 'read'):
            if hasattr(pdf_object, 'seek'):
                pdf_object.seek(0)
            data = pdf_object.read()
            if hasattr(pdf_object, 'seek'):
                pdf_object.seek(0)
            return data

        raise TypeError("Argument must be bytes or a valid file-like object.")

    def compress_pdf(self, pdf_object):
        comando_gs = 'gs' if os.name != 'nt' else 'gswin64c'
        pdf_bytes_content = self._extract_bytes(pdf_object)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as in_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as out_file:
            try:
                in_file.write(pdf_bytes_content)
                in_file.close()
                out_file.close()

                comando = [
                    comando_gs,
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    "-dPDFSETTINGS=/ebook",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    f"-sOutputFile={out_file.name}",
                    in_file.name
                ]
                
                subprocess.run(comando, check=True, capture_output=True)
                
                with open(out_file.name, 'rb') as f:
                    compressed_pdf = f.read()
                
                return compressed_pdf

            finally:
                if os.path.exists(in_file.name):
                    os.unlink(in_file.name)
                if os.path.exists(out_file.name):
                    os.unlink(out_file.name)

    def compress_several_pdfs(self, files_list):
        compressed_list = []
        for file in files_list:
            compressed_list.append(self.compress_pdf(file))
        return compressed_list

    def merge_several_pdfs(self, files_list, merged_name=None):
        merger = PdfWriter()
        for file in files_list:
            pdf_bytes = self._extract_bytes(file)
            merger.append(io.BytesIO(pdf_bytes))

        temp_buffer = io.BytesIO()
        merger.write(temp_buffer)
        temp_buffer.seek(0)
        return temp_buffer.getvalue()

    def compress_and_merge(self, files_list):
        compressed_list = []

        for file in files_list:
            # Obtém o tamanho correto dependendo do tipo do objeto
            if hasattr(file, 'size'):
                file_size = file.size
            elif isinstance(file, bytes):
                file_size = len(file)
            else:
                pdf_bytes = self._extract_bytes(file)
                file_size = len(pdf_bytes)

            if file_size > self.limit_MB_file * 1024**2:
                raise ValueError(f"File size exceeds the limit of {self.limit_MB_file} MB.")

            compressed_list.append(self.compress_pdf(file))

        merger = PdfWriter()
        for compressed in compressed_list:
            merger.append(io.BytesIO(compressed))

        temp_buffer = io.BytesIO()
        merger.write(temp_buffer)
        temp_buffer.seek(0)
        return temp_buffer.getvalue()