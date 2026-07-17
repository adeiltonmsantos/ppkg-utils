import io
import os
import subprocess
import tempfile

from pypdf import PdfWriter


class PdfCompressor():
    """
    PdfCompressor
    -------------
    A class that can compress PDF files and merge then into a single file, given a limit in MB per file
    """

    def __init__(self, limit_MB_file=20):
        self.limit_MB_file = limit_MB_file

    def compress_pdf(self, pdf_object):
        """
        compress_pdf(path_in, path_out)
        -------------------------------
        Uses Ghostscript to compress a PDF file:
        """
        # In Windows, the command usually is 'gswin64c'. In Linux/Mac, it's 'gs'.
        comando_gs = 'gs' if os.name != 'nt' else 'gswin64c'
        
        # If PDF is pure bytes in memory
        if isinstance(pdf_object, bytes):
            pdf_bytes_content = pdf_object
            
        # If PDF is a file in Django memory (InMemoryUploadedFile) or BytesIO
        elif hasattr(pdf_object, 'read'):
            # Garante que o ponteiro de leitura está no início do arquivo antes de ler
            if hasattr(pdf_object, 'seek'):
                pdf_object.seek(0)
            pdf_bytes_content = pdf_object.read()
            
        else:
            raise TypeError("Argument must be bytes or a valid file object.")

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
                    # dPDFSETTINGS defines the compression level:
                    # /screen   (low resolution, ideal for screens, smaller sizes)
                    # /ebook    (meddium resolution, geate balance)
                    # /printer  (higher resolution to print)
                    "-dPDFSETTINGS=/ebook",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    f"-sOutputFile={out_file.name}",
                    in_file.name
                ]
                subprocess.run(comando, check=True)
                with open(out_file.name, 'rb') as f:
                    compressed_pdf = f.read()
                
                return compressed_pdf
            
            finally:
                if os.path.exists(in_file.name):
                    os.unlink(in_file.name)
                if os.path.exists(out_file.name):
                    os.unlink(out_file.name)        

    def compress_and_merge(self, files_list):
        """
        compress_and_merge(files_list, limit_in_MB, filename_merged, folder_temp=None)
        ---------------------------------------------------
        Method that waits a list with in-memory PDF files to compress and merge:
        - files_list: list with in-memory PDF files to compress and merge
        - limit_in_MB: maximum merged file size
        - filename_merged: name of the merged file. If the compressed and merged file exceed LIMIT_MB
        in size, multiple files are created (filename_merged01.pdf, filename_merged02.pdf, etc.)
        """

        # Compressing files in files_list
        try:
            compressed_list = []

            for file in files_list:
                if len(file) > self.limit_MB_file * 1024**2:
                    raise(f"There's file in files_list higher then {self.limit_MB_file}")
            
                compressed_list.append(self.compress_pdf(file))
            
            # Merging files...
            merger = PdfWriter() # Object that merge files

            for compressed in compressed_list:
                merger.append(io.BytesIO(compressed))
        
            temp_buffer = io.BytesIO()
            merger.write(temp_buffer)
            temp_buffer.seek(0)
            return temp_buffer.getvalue()
        except Exception as e:
            raise(f'files_list must be a list, even if only one file: {e}')
