# views.py

from django.shortcuts import render, redirect
from .models import Post, PostImage  # Removido o import de Publicacao, agora usamos apenas Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

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
        return redirect('feed')


# views.py (classe PostCreateView)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social/create_post.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        images = self.request.FILES.getlist('images')
        for i, image in enumerate(images[:5]):  # limita a 5 imagens
            PostImage.objects.create(post=self.object, image=image)

        return response


class PostDetailView(DetailView):
    """
    Exibe os detalhes de uma postagem.
    """
    model = Post  # Utiliza o modelo Post
    template_name = 'social/post_detail.html'  # Atualize o template conforme necessário
    context_object_name = 'post'  # Nome do objeto no contexto
