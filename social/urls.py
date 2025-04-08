from django.urls import path
from .views import *
from . import views

app_name = 'social'

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),

    path('feed/more/', views.feed_more_view, name='feed_more'),

    path('nova-postagem/', PostTypeSelectView.as_view(), name='nova_postagem_select'),
    path('nova-postagem/normal/', NormalPostCreateView.as_view(), name='nova_postagem_normal'),
    path('nova-postagem/carousel/', CarouselPostCreateView.as_view(), name='nova_postagem_carousel'),
    path('nova-postagem/poll/', PollPostCreateView.as_view(), name='nova_postagem_poll'),
    path('nova-postagem/event/', EventPostCreateView.as_view(), name='nova_postagem_event'),
    path('nova-postagem/bikeroute/', BikeRoutePostCreateView.as_view(), name='nova_postagem_bikeroute'),
    
    path('upload-image/', views.upload_image, name='upload_image'),

    path('publicacao/<int:pk>/', PostDetailView.as_view(), name='publicacao_detalhe'),
]
