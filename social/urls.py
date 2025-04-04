from django.urls import path
from .views import (
    feed_view,
    PostTypeSelectView,
    PostDetailView,
    NormalPostCreateView,
    CarouselPostCreateView,
    PollPostCreateView,
    EventPostCreateView,
    BikeRoutePostCreateView,
    
)
from . import views  # Importa views.py para usar feed_more_view como FBV

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),

    path('feed/more/', views.feed_more_view, name='feed_more'),

    path('nova-postagem/', PostTypeSelectView.as_view(), name='nova_postagem_select'),
    path('nova-postagem/normal/', NormalPostCreateView.as_view(), name='nova_postagem_normal'),
    path('nova-postagem/carousel/', CarouselPostCreateView.as_view(), name='nova_postagem_carousel'),
    path('nova-postagem/poll/', PollPostCreateView.as_view(), name='nova_postagem_poll'),
    path('nova-postagem/event/', EventPostCreateView.as_view(), name='nova_postagem_event'),
    path('nova-postagem/bikeroute/', BikeRoutePostCreateView.as_view(), name='nova_postagem_bikeroute'),

    path('publicacao/<int:pk>/', PostDetailView.as_view(), name='publicacao_detalhe'),
]
