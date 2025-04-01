# accounts/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.conf import settings

from accounts.forms import CustomUserCreationForm

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'  # Template de cadastro
    form_class = CustomUserCreationForm        # Formulário que inclui o campo email
    success_url = reverse_lazy('profile')       # URL para redirecionamento após cadastro

    def form_valid(self, form):
        # Salva o formulário e obtém a resposta padrão
        response = super().form_valid(form)
        # Realiza o login automático do usuário após o cadastro
        login(self.request, self.object)
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View para exibir o perfil do usuário logado.
    O mixin LoginRequiredMixin garante que somente usuários autenticados possam acessar.
    """
    template_name = 'accounts/profile.html'


class CustomLogoutView(View):
    """
    View customizada para fazer logout tanto via GET quanto POST.
    Reforça o logout de forma explícita, chamando logout(request).
    """
    def dispatch(self, request, *args, **kwargs):
        # Sempre que acessar essa view, desloga o usuário
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
