# models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType  # Para o sistema de relatórios
from django.contrib.contenttypes.fields import GenericForeignKey
import re
from django.contrib.auth.models import User
from django.conf import settings


# Obtém o modelo de usuário (suporte a modelos customizados)
User = get_user_model()

###############################################
# MODELOS RELACIONADOS A POSTS E FUNCIONALIDADES
###############################################

# Modelo para Categorias
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nome único para a categoria

    def __str__(self):
        return self.name

# Modelo para Tags
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nome único para a tag

    def __str__(self):
        return self.name

# Modelo principal de Post com diversas funcionalidades
class Post(models.Model):
    # Relação com o usuário que criou o post
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # Campos básicos do post
    title = models.CharField(max_length=200, blank=True, null=True)  # Título opcional
    content = models.TextField(blank=True, null=True)  # Conteúdo do post
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização

    # Contadores (incluindo o de curtidas)
    edit_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)  # Contador de curtidas
    comments_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    # Localização
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Link compartilhado e visibilidade
    shared_link = models.URLField(blank=True, null=True)
    VISIBILITY_CHOICES = [
        ('public', 'Público'),
        ('friends', 'Amigos'),
        ('private', 'Privado'),
    ]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')

    # Campos para eventos e trajeto de bike
    is_event = models.BooleanField(default=False)
    event_date = models.DateTimeField(blank=True, null=True)
    bike_trajectory = models.JSONField(blank=True, null=True)

    # Relacionamentos ManyToMany (categorias, tags, etc.) podem existir aqui

    def __str__(self):
        # Representa o post com o nome do usuário e data de criação
        return f"{self.user.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    def is_youtube_link(self):
        """
        Verifica se o link compartilhado é do YouTube.
        Retorna True se 'youtube.com' ou 'youtu.be' estiver presente na URL.
        """
        if self.shared_link:
            return bool(re.search(r'(youtube\.com|youtu\.be)', self.shared_link, re.IGNORECASE))
        return False

# Novo modelo para registrar as curtidas dos posts
class PostLike(models.Model):
    # Associa o like ao post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    # Associa o like ao usuário que o realizou
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    liked_at = models.DateTimeField(auto_now_add=True)  # Data e hora em que o like foi realizado

    class Meta:
        # Garante que cada usuário possa curtir um post somente uma vez
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} curtiu {self.post.pk} em {self.liked_at}"

###############################################
# MODELO PARA IMAGENS ASSOCIADAS AO POST
###############################################

class PostImage(models.Model):
    # Cada imagem está relacionada a um post específico
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')  # Armazena a imagem na pasta 'posts/'

    def __str__(self):
        return f"Imagem de {self.post.user.username}"

###############################################
# MODELO PARA COMENTÁRIOS COM REPLIES (ANINHADOS)
###############################################

class Comment(models.Model):
    # Relação com o post em que o comentário foi feito
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Usuário que fez o comentário
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # Conteúdo do comentário
    content = models.TextField()
    # Data e hora em que o comentário foi criado
    created_at = models.DateTimeField(auto_now_add=True)
    # Comentário pai para suportar respostas (comentários aninhados)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        # Exibe o usuário e o ID do post, indicando se é resposta
        if self.parent:
            return f"Reply de {self.user.username} ao comentário {self.parent.id}"
        return f"Comentário de {self.user.username} no post {self.post.id}"

###############################################
# MODELO DE ENQUETE (POLL) E MELHORIAS
###############################################

# Modelo de enquete vinculado a um post
class Poll(models.Model):
    # Relação de um para um com o post (enquete é parte de um post)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=255)  # Pergunta da enquete
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação da enquete
    expiration_date = models.DateTimeField(blank=True, null=True)  # Data de expiração da enquete

    def __str__(self):
        return f"Enquete: {self.question} (Post: {self.post.id})"

# Modelo para as opções da enquete
class PollOption(models.Model):
    # Cada opção pertence a uma enquete
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)  # Texto da opção
    votes_count = models.PositiveIntegerField(default=0)  # Contador de votos para a opção

    def __str__(self):
        return f"Opção: {self.option_text} (Votos: {self.votes_count})"

# Modelo para registrar o voto de um usuário em uma enquete
class Vote(models.Model):
    # Relaciona o voto à enquete
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    # Indica qual opção foi escolhida
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    # Usuário que votou
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    # Data em que o voto foi registrado
    voted_at = models.DateTimeField(auto_now_add=True)
    # Data da última edição do voto (caso o usuário altere sua escolha)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Garante que cada usuário vote apenas uma vez por enquete
        unique_together = ('poll', 'user')

    def __str__(self):
        return f"Voto de {self.user.username} na enquete {self.poll.id} - Opção: {self.option.option_text}"

###############################################
# MODELO DE RELATÓRIOS E MODERAÇÃO
###############################################

class Report(models.Model):
    # Usuário que está fazendo o relatório
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    # Campo genérico para associar o relatório a um post ou comentário
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reported_object = GenericForeignKey('content_type', 'object_id')
    # Motivo do relatório
    reason = models.CharField(max_length=255)
    # Data em que o relatório foi criado
    created_at = models.DateTimeField(auto_now_add=True)
    # Status do relatório (ex: pendente, revisado, resolvido)
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('reviewed', 'Revisado'),
        ('resolved', 'Resolvido'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Relatório por {self.reporter.username} em {self.content_type} {self.object_id} - Status: {self.status}"

###############################################
# MODELOS PARA RELAÇÕES DE AMIZADE E SEGUIDORES
###############################################

# Modelo para solicitações de amizade e relações de amizade
class Friendship(models.Model):
    # Usuário que envia o pedido de amizade
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_sent')
    # Usuário que recebe o pedido de amizade
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    # Indica se o pedido foi aceito
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Data em que o pedido foi enviado

    class Meta:
        unique_together = ('from_user', 'to_user')
        # Garante que não existam solicitações duplicadas

    def __str__(self):
        status = "Aceita" if self.accepted else "Pendente"
        return f"Amizade de {self.from_user.username} para {self.to_user.username} - {status}"

# Modelo para seguir outros usuários (relação unidirecional)
class Follow(models.Model):
    # Usuário que está seguindo outro
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    # Usuário que está sendo seguido
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)  # Data em que a relação foi criada

    class Meta:
        unique_together = ('follower', 'following')
        # Garante que um usuário não siga outro mais de uma vez

    def __str__(self):
        return f"{self.follower.username} segue {self.following.username}"
