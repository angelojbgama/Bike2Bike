# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, ProfileView

urlpatterns = [
    # Login (CBV nativa)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Logout (CBV nativa; redireciona para 'login' após logout)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Cadastro de usuário (CBV personalizada)
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Perfil do usuário (apenas para usuários autenticados)
    path('profile/', ProfileView.as_view(), name='profile'),
]
