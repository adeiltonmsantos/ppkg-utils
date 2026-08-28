from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm


class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'appUsers/pages/registration_user.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Usuário(a) cadastrado(a) com sucesso!'

    def get_context_data(self, *args, **kwargs):
        cnt = super().get_context_data(**kwargs)
        cnt['title_page'] = 'Cadastro de Usuário'
        return cnt
