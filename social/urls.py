from django.urls import path
from .views import (
    feed_view,
    PostCreateView,
    PostDetailView,
)
from . import views  # Importa views.py para usar feed_more_view como FBV

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),

    path('feed/more/', views.feed_more_view, name='feed_more'),

    path('nova-postagem/', PostCreateView.as_view(), name='nova_postagem'),

    path('publicacao/<int:pk>/', PostDetailView.as_view(), name='publicacao_detalhe'),
]
