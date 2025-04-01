# accounts/views.py
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

from django.conf import settings
from .forms import CustomUploadAvatarForm
from django.contrib import messages
from django.utils.translation import gettext as _

from avatar.models import Avatar

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
    
# Exemplo de view baseada em classe
class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile.html'
    form_class = CustomUploadAvatarForm  # Importante: usar o formulário que tem o DaisyUI mixin
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Lógica para salvar o avatar
        avatar_image = form.cleaned_data["avatar"]
        avatar = Avatar(user=self.request.user, primary=True)
        avatar.avatar.save(avatar_image.name, avatar_image)
        avatar.save()
        messages.success(self.request, "Avatar atualizado com sucesso!")
        return super().form_valid(form)

class CustomLogoutView(View):
    """
    View customizada para fazer logout tanto via GET quanto POST.
    Reforça o logout de forma explícita, chamando logout(request).
    """
    def dispatch(self, request, *args, **kwargs):
        # Sempre que acessar essa view, desloga o usuário
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
