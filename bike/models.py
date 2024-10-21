from django.db import models

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
    Model para cadastro de lugares, incluindo nome, descricão, latitude e longitude.
    """
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Utilizamos choices para limitar os tipos de lugar às opções da constante
    tipo = models.CharField(
        max_length=50,
        choices=[(key, value) for key, value in TIPOS_DE_LUGARES.items()],
        default='parque'
    )

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def get_comentarios(self):
        """
        Retorna todos os comentários associados a este lugar.
        """
        return self.comentarios.all()


class Comentario(models.Model):
    """
    Model para comentários feitos por qualquer visitante sobre um lugar específico.
    """
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário em {self.lugar.nome} em {self.data_criacao}"
