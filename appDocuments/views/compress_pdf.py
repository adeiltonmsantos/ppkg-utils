
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from utils.pdf_compress import PdfCompressor

from ..forms import CompressPdfForm


class CompressPdfView(FormView):
    template_name = 'appDocuments/pages/compress-pdf.html'
    form_class = CompressPdfForm
    success_url = reverse_lazy('appDocuments/pages/compress-pdf.html')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title_form'] = 'Comprimir PDFs'
        return ctx

    def form_valid(self, form):
        # Getting username of logged-in user
        username = self.request.user.username

        # Defining user folder name
        # user_folder = Path(f'MEDIA/{username}')

        user_dir_relative = f'{username}'

        # Cleaning older files
        try:
            directories, files = default_storage.listdir(user_dir_relative)  # noqa: RUF059
            for file_name in files:
                if file_name.startswith(username) and file_name.endswith('.pdf'):
                    default_storage.delete(f'{user_dir_relative}/{file_name}')
        except FileNotFoundError:
            pass

        # Getting files to compress in a list
        pdf_list = form.cleaned_data['pdf_files']
        main_filename = form.cleaned_data['main_filename']

        # Instantiating PdfCOmpressor object 
        compressor = PdfCompressor()

        # Getting list of in-memory compressed files
        pdf_list_compressed = compressor.compress_several_pdfs(pdf_list)

        # Creating variable to set list of compressed files URLs
        compressed_files_list = []

        # Saving in-memory compressed files in user folder in MEDIA
        for i, file_bytes in enumerate(pdf_list_compressed, start=1):
            current_filename_path = f'{username}/{main_filename}-{i}.pdf'

            if default_storage.exists(current_filename_path):
                default_storage.delete(current_filename_path)

            saved_path = default_storage.save(current_filename_path, ContentFile(file_bytes))
            compressed_files_list.append(
                {
                    'name': f'{main_filename}-{i}.pdf',
                    'url': default_storage.url(saved_path),
                    'size': len(file_bytes) / (1024**2)
                }
            )

        # Getting context data
        context = self.get_context_data(form=form)
        context['compressed_files_list'] = compressed_files_list
        
        return self.render_to_response(context)
    