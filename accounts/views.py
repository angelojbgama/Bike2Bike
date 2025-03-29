# accounts/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    """
    View para cadastro de novos usuários.
    Utiliza o UserCreationForm padrão do Django.
    Após a criação do usuário, faz login automaticamente e redireciona para o perfil.
    """
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profile')  # Redireciona para a página de perfil após cadastro

    def form_valid(self, form):
        # Salva o usuário (self.object será o novo usuário)
        response = super().form_valid(form)
        # Faz login do usuário recém-criado
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View para exibir o perfil do usuário logado.
    O mixin LoginRequiredMixin garante que somente usuários autenticados possam acessar.
    """
    template_name = 'accounts/profile.html'
