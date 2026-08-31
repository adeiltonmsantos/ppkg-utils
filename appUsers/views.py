from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm


class UserRegistrationView(LoginRequiredMixin, CreateView):
    template_name = 'appUsers/pages/registration_user.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        cnt = super().get_context_data(**kwargs)
        cnt['title_page'] = 'Cadastro de Usuário'
        return cnt

    def form_valid(self, form):
        messages.success(self.request, 'Usuário(a) cadastrado(a) com sucesso!')
        return super().form_valid(form)
    