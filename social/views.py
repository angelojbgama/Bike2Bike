from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacao
from .forms import PostForm

def feed_view(request):
    posts = Publicacao.objects.all()
    return render(request, 'social/feed.html', {'posts': posts})

def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})

# 🔍 Nova view de detalhe da publicação
def post_detalhe_view(request, pk):
    post = get_object_or_404(Publicacao, pk=pk)
    return render(request, 'social/publicacao_detalhe.html', {'post': post})
