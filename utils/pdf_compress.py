import os
import subprocess
from pathlib import Path

from pypdf import PdfWriter


class PdfCompressor():
    def compress_pdf(self, path_in, path_out):
        """
        Usa o Ghostscript para re-amostrar e comprimir o PDF inteiro.
        """
        # No Windows, o comando geralmente é 'gswin64c'. No Linux/Mac, é 'gs'.
        comando_gs = 'gs' if os.name != 'nt' else 'gswin64c'
        
        comando = [
            comando_gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            # dPDFSETTINGS define o nível de compressão:
            # /screen   (baixa resolução, ideal para telas, menor tamanho)
            # /ebook    (média resolução, ótimo balanço)
            # /printer  (alta resolução para impressão)
            "-dPDFSETTINGS=/ebook", 
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={path_out}",
            path_in
        ]
        
        try:
            subprocess.run(comando, check=True)
            print("PDF comprimido com sucesso pelo Ghostscript!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao comprimir: {e}")

    def compress_and_merge(self, files_path, filename_merged, limit_in_MB):
        """
        compress_and_merge(filenames_list, filename_merged)

        Method that waits a list with paths of the PDF files to compress and merge (filenames_list),
        a file name of the merged files (filename_merged) and the maximum size in Megabytes of the 
        compressed and merged file (limit_in_MB). If the size limit is superior than limit_in_MB 
        several files are created (filename_merged01.pdf, filename_merged02.pdf, etc.)
        """

        size = 0
        merger = PdfWriter()
        path = Path(files_path)
        filenames_list = path.glob('*.pdf')
        i = 0
        for filename in filenames_list:
            i += 1
            path_in = str(filename)
            path_out = f'compressed_and_merged.pdf{i:02d}'
            self.compress_pdf(path_in, path_out)
            # Calculating size in MB of file compressed
            filesize = Path(path / f'{path_out}.pdf').stat().st_size / (1024 * 1024)