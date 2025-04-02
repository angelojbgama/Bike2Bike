from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacao
from .forms import PostForm
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse

def feed_view(request):
    """
    Renderiza o feed inicial.
    Recupera todos os posts (ordenados dos mais recentes para os mais antigos)
    e pagina em blocos de 5 posts.
    """
    posts = Publicacao.objects.all().order_by('-criado_em')
    paginator = Paginator(posts, 5)  # 5 posts por página
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
        paginator = Paginator(posts, 5)  # Mesmo número de posts por página
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

def create_post_view(request):
    """
    View para criar uma nova publicação.
    - Se for POST, processa os dados do formulário.
    - Se for GET, exibe o formulário vazio.
    """
    if request.method == 'POST':
        # Cria o formulário com os dados enviados (incluindo arquivos, se houver)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Cria a publicação sem salvar imediatamente (para definir o autor)
            post = form.save(commit=False)
            post.autor = request.user  # Define o autor como o usuário logado
            post.save()  # Salva a publicação no banco de dados
            return redirect('feed')  # Redireciona para o feed após criar o post
    else:
        # Cria um formulário vazio para GET
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})

# 🔍 Nova view de detalhe da publicação
def post_detalhe_view(request, pk):
    post = get_object_or_404(Publicacao, pk=pk)
    return render(request, 'social/publicacao_detalhe.html', {'post': post})
