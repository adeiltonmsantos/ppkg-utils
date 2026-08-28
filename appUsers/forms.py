from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-input',
                'placeholder': 'Digite seu login aqui',
                'width': '40%',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-text-input',
                'placeholder': 'Digite sua senha aqui',
                'width': '40%'
            }
        )
    )

class UserRegistrationForm(UserCreationForm):
    # Defining 'nome' field to form
    nome = forms.CharField(
        max_length=150,
        required=True,
        label='Nome'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('nome', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.cleaned_data['nome']
        if commit:
            user.save()
        return user