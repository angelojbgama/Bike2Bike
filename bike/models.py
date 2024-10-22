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
    """
    Model para cadastro de lugares, incluindo nome, descrição, latitude e longitude.
    """
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Utilizamos choices para limitar os tipos de lugar às opções da constante
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_DE_LUGARES.items(),
        default='parque'
    )

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def get_comentarios(self):
        """
        Retorna todos os comentários associados a este lugar.
        """
        return self.comentarios.all()
    
    def media_estrelas(self):
        """
        Calcula a média das estrelas dos comentários associados a este lugar.
        """
        media = self.comentarios.aggregate(Avg('estrelas'))['estrelas__avg']
        return round(media, 2) if media else 0

    def soma_estrelas(self):
        """
        Soma todas as estrelas dos comentários para este lugar.
        """
        soma = self.comentarios.aggregate(Sum('estrelas'))['estrelas__sum']
        return soma if soma else 0

    def calcular_media_estrelas(self):
        """
        Calcula a média das avaliações em estrelas para este lugar.
        """
        comentarios = self.comentarios.all()
        total_estrelas = sum(comentario.estrelas for comentario in comentarios)
        return total_estrelas / comentarios.count() if comentarios.exists() else 0


class Comentario(models.Model):
    """
    Model para comentários feitos por visitantes sobre um lugar específico com avaliação em estrelas.
    """
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Permitir valores de 0 a 5 estrelas
    estrelas = models.PositiveSmallIntegerField(
        default=0,  # Valor padrão alterado para 0
        validators=[
            MinValueValidator(0, message="A avaliação pode começar com 0 estrelas."),
            MaxValueValidator(5, message="A avaliação pode ter no máximo 5 estrelas.")
        ],
        help_text="Avaliação de 0 a 5 estrelas"
    )

    def __str__(self):
        return f"Comentário em {self.lugar.nome} - {self.estrelas} estrelas em {self.data_criacao}"

    def soma_estrelas(self):
        """
        Retorna a soma das estrelas de todas as avaliações relacionadas a este comentário.
        """
        return self.lugar.comentarios.aggregate(Sum('estrelas'))['estrelas__sum'] or 0
