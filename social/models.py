# social/models.py
from django.db import models
from django.contrib.auth import get_user_model

# Utiliza o modelo de usuário padrão configurado no projeto
Usuario = get_user_model()

# Modelo de Publicação
class Publicacao(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="publicacoes")
    conteudo = models.TextField(verbose_name="Conteúdo")
    imagem = models.ImageField(upload_to='publicacoes/', blank=True, null=True, verbose_name="Imagem")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return f"{self.autor.username} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"
        ordering = ['-criado_em']


# Modelo de Comentário
class Comentario(models.Model):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField(verbose_name="Comentário")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data do Comentário")

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.criado_em.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['criado_em']
