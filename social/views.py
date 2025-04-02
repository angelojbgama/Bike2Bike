from django.shortcuts import render, redirect
from .models import Publicacao
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
    e pagina em blocos de 5 posts.
    """
    posts = Publicacao.objects.all().order_by('-criado_em')
    paginator = Paginator(posts, 3)  # 5 posts por página
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
    # Verifica se é uma requisição AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        posts = Publicacao.objects.all().order_by('-criado_em')
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

class PublicacaoCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova publicação.
    Requer que o usuário esteja logado.
    """
    model = Publicacao
    form_class = PostForm
    template_name = 'social/create_post.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PublicacaoDetailView(DetailView):
    """
    Exibe os detalhes de uma publicação.
    """
    model = Publicacao
    template_name = 'social/publicacao_detalhe.html'
    context_object_name = 'post'
