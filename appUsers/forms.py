from django import forms
from django.contrib.auth.forms import AuthenticationForm


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