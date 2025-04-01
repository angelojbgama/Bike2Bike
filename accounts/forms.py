from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from bike2bike.mixins.DaisyUIFormMixin import DaisyUIStyledFormMixin



class CustomUserCreationForm(DaisyUIStyledFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Informe um e-mail válido.'
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        field_styles = {
            "username": {
                "classes": "input-primary input-md",
                "type": "text",  # aqui você define o type do input
                "icon": '<i class="fa fa-user h-[1em] opacity-50"></i>',
                "placeholder": "Usuário",
                "wrapper_class": "w-full",
                "row_class": "mb-4",
            },
            "email": {
                "classes": "input-info",
                "placeholder": "mail@site.com",
                "icon": '<i class="fa fa-envelope h-[1em] opacity-50"></i>',
                "row_class": "mb-4",

            },
            "password1": {
                "classes": "input-success",
                "icon": '<i class="fa fa-key h-[1em] opacity-50"></i>',
                "placeholder": "Senha forte",
                "hint": "Use pelo menos uma letra maiúscula, minúscula e um número",
                "type": "password",
                "pattern": "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "title": "Senha segura com maiúscula, minúscula e número",
                "row_class": "mb-4",

            },
            "password2": {
                "classes": "input-success",
                "icon": '<i class="fa fa-key h-[1em] opacity-50"></i>',
                "placeholder": "Senha forte",
                "hint": "Use pelo menos uma letra maiúscula, minúscula e um número",
                "type": "password",
                "pattern": "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "title": "Senha segura com maiúscula, minúscula e número",
                "row_class": "mb-4",
            },
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(DaisyUIStyledFormMixin, AuthenticationForm):
    """
    Formulário customizado de autenticação que utiliza o DaisyUIStyledFormMixin
    para aplicar estilos customizados aos campos.
    
    Os campos padrão do AuthenticationForm são "username" e "password".
    """
    class Meta:
        # Define os estilos para cada campo utilizando o dicionário field_styles
        field_styles = {
            "username": {
                "classes": "input-primary input-md",
                "icon": '<i class="fa fa-user mr-[0.3em] h-[1em] opacity-50"></i>',
                "type": "text",
                "placeholder": "Seu usuário",  # Placeholder do campo
                "row_class": "mb-4",
                "autocomplete": "off",# Classe para adicionar espaçamento inferior
            },
            "password": {
                "classes": "input-neutral grow",
                "icon": '<i class="fa fa-key h-[1em] opacity-50"></i>',
                "type":"password",# Classe aplicada ao input da senha
                "placeholder": "Sua senha",  # Placeholder do campo
                "row_class": "mb-4",
                "autocomplete": "off",# Classe para espaçamento inferior
            },
        }