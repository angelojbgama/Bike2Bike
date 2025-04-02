from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('postar/', views.create_post_view, name='create_post'),
    path('publicacao/<int:pk>/', views.post_detalhe_view, name='publicacao_detalhe'),  # ← novo
]
