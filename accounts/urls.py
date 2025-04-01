# accounts/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts.forms import CustomAuthenticationForm
from .views import CustomLogoutView, SignUpView, ProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Login e logout
    path('login/', auth_views.LoginView.as_view( template_name='accounts/login.html', authentication_form=CustomAuthenticationForm ), name='login' ), 
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Recuperação de senha por e-mail
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
