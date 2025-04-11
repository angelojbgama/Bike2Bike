from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('feed/more/', views.feed_more_view, name='feed_more'),
    path('nova-postagem/', views.PostTypeSelectView.as_view(), name='nova_postagem_select'),
    path('nova-postagem/normal/', views.NormalPostCreateView.as_view(), name='nova_postagem_normal'),
    path('nova-postagem/carousel/', views.CarouselPostCreateView.as_view(), name='nova_postagem_carousel'),
    path('nova-postagem/poll/', views.PollPostCreateView.as_view(), name='nova_postagem_poll'),
    path('nova-postagem/event/', views.EventPostCreateView.as_view(), name='nova_postagem_event'),
    path('nova-postagem/bikeroute/', views.BikeRoutePostCreateView.as_view(), name='nova_postagem_bikeroute'),
    path('upload-image/', views.upload_image, name='upload_image'),
    # URL para processar a ação de curtir
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('publicacao/<int:pk>/', views.PostDetailView.as_view(), name='publicacao_detalhe'),
    path('post/<int:post_id>/comentar-htmx/', views.comentar_post_htmx, name='comentar_post_htmx'),

]
