from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Sum

# Constante para os tipos de lugares
TIPOS_DE_LUGARES = {
    'parque': 'Parque público',
    'museu': 'Museu ou galeria de arte',
    'restaurante': 'Restaurante ou café',
    'hotel': 'Hotel ou hospedagem',
    'mercado': 'Supermercado ou feira',
    'bike_reparo': 'Reparo de bicicleta',
}

class Lugar(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_DE_LUGARES.items(),
        default='parque'
    )

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def get_comentarios(self):
        """Retorna todos os comentários associados a este lugar."""
        return self.comentarios.all()

    def media_estrelas(self):
        """Calcula a média das estrelas de todas as avaliações do lugar."""
        comentarios = self.get_comentarios()
        total_avaliacoes = sum([c.avaliacoes.count() for c in comentarios]) + len(comentarios)
        soma_estrelas = sum([c.soma_estrelas() for c in comentarios])

        if total_avaliacoes > 0:
            return round(soma_estrelas / total_avaliacoes, 2)
        return 0

    def soma_estrelas(self):
        """Calcula a soma total das estrelas de todos os comentários e suas avaliações."""
        return sum([c.soma_estrelas() for c in self.get_comentarios()])

    def total_avaliacoes(self):
        """Conta o total de avaliações (comentários + avaliações associadas)."""
        comentarios = self.get_comentarios()
        return sum([c.avaliacoes.count() for c in comentarios]) + len(comentarios)


class Comentario(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    estrelas = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Avaliação de 0 a 5 estrelas"
    )

    def __str__(self):
        return f"Comentário em {self.lugar.nome} - {self.estrelas} estrelas"

    def soma_estrelas(self):
        """Soma as estrelas deste comentário e suas avaliações."""
        avaliacao_sum = self.avaliacoes.aggregate(soma=Sum('estrelas'))['soma'] or 0
        return int(self.estrelas) + int(avaliacao_sum)


class AvaliacaoComentario(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='avaliacoes')
    estrelas = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Avaliação de 1 a 5 estrelas"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estrelas} estrelas - Comentário {self.comentario.pk}"
