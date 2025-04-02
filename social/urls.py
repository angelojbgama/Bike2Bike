from django.urls import path
from .views import (
    feed_view,
    PublicacaoCreateView,
    PublicacaoDetailView,
)
from . import views  # Importa views.py para usar feed_more_view como FBV

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),

    path('feed/more/', views.feed_more_view, name='feed_more'),

    path('postar/', PublicacaoCreateView.as_view(), name='create_post'),

    path('publicacao/<int:pk>/', PublicacaoDetailView.as_view(), name='publicacao_detalhe'),
]
