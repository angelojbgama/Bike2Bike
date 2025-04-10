# views.py

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import TemplateView

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

import json
from .models import Post, PostImage, Poll, PollOption
from .forms import CarouselPostForm, PollPostForm, EventPostForm, BikeRoutePostForm, NormalPostForm


def feed_view(request):
    """
    Renderiza o feed inicial.
    Recupera todos os posts (ordenados dos mais recentes para os mais antigos)
    e pagina em blocos de 3 posts.
    """
    # Alterado de Publicacao para Post e do campo 'criado_em' para 'created_at'
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)  # Paginação: 3 posts por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # Página atual de posts
    }
    return render(request, 'social/feed.html', context)


def feed_more_view(request):
    """
    View para carregar mais posts via AJAX.
    Recebe o número da página via GET, pagina os posts e renderiza um template parcial
    contendo os posts da página solicitada.
    Retorna um JSON com o HTML renderizado e informações de paginação.
    """
    # Verifica se a requisição é AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Alterado de Publicacao para Post e do campo 'criado_em' para 'created_at'
        posts = Post.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 3)  # Mesmo número de posts por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Renderiza o template parcial com a lista de posts
        html = render_to_string('social/_post_list.html', {'page_obj': page_obj}, request=request)
        data = {
            'html': html,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        }
        return JsonResponse(data)
    else:
        return redirect('social:feed')

class PostTypeSelectView(LoginRequiredMixin, TemplateView):
    template_name = "social/posts/select_post_type.html"
    

class CarouselPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CarouselPostForm
    template_name = "social/posts/create_carousel_post.html"
    success_url = reverse_lazy("social:feed")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist("images")
        for image in images:
            PostImage.objects.create(post=self.object, image=image)
        return response


class PollPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PollPostForm
    template_name = "social/posts/create_poll_post.html"
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        poll_options_str = form.cleaned_data.get("poll_options")
        if poll_options_str:
            poll = Poll.objects.create(
                post=self.object,
                question=form.cleaned_data.get("title") or "Enquete"
            )
            options = [opt.strip() for opt in poll_options_str.split(",") if opt.strip()]
            for option_text in options:
                PollOption.objects.create(poll=poll, option_text=option_text)
        return response
class EventPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = EventPostForm
    template_name = "social/posts/create_event_post.html"
    success_url = reverse_lazy("social:feed")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class BikeRoutePostCreateView(LoginRequiredMixin, CreateView):
    """
    View para criação de posts de trajeto de bike.
    O usuário define a rota clicando no mapa e os dados são enviados via campo oculto.
    """
    model = Post
    form_class = BikeRoutePostForm
    template_name = "social/posts/create_bikeroute_post.html"
    success_url = reverse_lazy("social:feed")

    def form_valid(self, form):
        # Associa o post ao usuário logado
        form.instance.user = self.request.user
        
        # Salva o objeto post inicialmente
        response = super().form_valid(form)
        
        # Recupera os dados da trajetória enviados via campo oculto (em formato JSON)
        bike_data = form.cleaned_data.get("bike_trajectory_data")
        if bike_data:
            try:
                # Converte os dados JSON para uma lista de pontos
                bike_trajectory = json.loads(bike_data)
                # Atribui a trajetória ao objeto post e salva a alteração
                self.object.bike_trajectory = bike_trajectory
                self.object.save()
            except json.JSONDecodeError:
                # Se houver erro na conversão, a trajetória não é salva e o fluxo continua
                pass
        return response

class NormalPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = NormalPostForm
    template_name = "social/posts/create_normal_post.html"
    success_url = reverse_lazy("social:feed")
    
    def form_valid(self, form):
        # Atribui o usuário logado ao post
        form.instance.user = self.request.user
        
        # Define a visibilidade do post, padrão 'public'
        form.instance.visibility = self.request.POST.get("visibility", "public")
        
        # --- Validação para posts apenas com texto ---
        # Recupera o conteúdo do post, assumindo que o campo de texto no formulário seja 'content'
        text = form.cleaned_data.get("content", "")
        
        # Verifica se o número de caracteres do texto excede 500
        if len(text) > 500:
            # Se exceder 500 caracteres, adiciona um erro específico ao campo 'content'
            form.add_error("content", "O texto não pode exceder 500 caracteres.")
            # Retorna o formulário inválido com os erros
            return self.form_invalid(form)
        
        # Se passar na validação, chama o método form_valid da classe pai para salvar o post
        return super().form_valid(form)


class PostDetailView(DetailView):
    """
    Exibe os detalhes de uma postagem.
    """
    model = Post  # Utiliza o modelo Post
    template_name = 'social/post_detail.html'  # Atualize o template conforme necessário
    context_object_name = 'post'  # Nome do objeto no contexto


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        filename = f"uploads/{uuid.uuid4()}_{image.name}"
        saved_path = default_storage.save(filename, ContentFile(image.read()))
        image_url = default_storage.url(saved_path)

        return JsonResponse({'success': True, 'url': image_url})
    return JsonResponse({'success': False}, status=400)
