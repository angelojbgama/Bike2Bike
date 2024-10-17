from django.db import models


TIPOS_DE_LUGARES = {
    'parque': 'Parque público',
    'museu': 'Museu ou galeria de arte',
    'restaurante': 'Restaurante ou café',
    'hotel': 'Hotel ou hospedagem',
    'mercado': 'Supermercado ou feira',
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
