from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm


class UserRegistrationView(CreateView):
    template_name = 'appUsers/pages/registration_user.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')