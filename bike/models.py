from django.db import models
from django.utils import timezone

# Constante para os tipos de lugares
TIPOS_DE_LUGARES = [
    ('parque', 'Parque público'),
    ('museu', 'Museu ou galeria de arte'),
    ('restaurante', 'Restaurante ou café'),
    ('hotel', 'Hotel ou hospedagem'),
    ('mercado', 'Supermercado ou feira'),
    ('bike_reparo', 'Reparo de bicicleta'),
]

class Lugar(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_DE_LUGARES,
        default='parque'
    )

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def get_comentarios(self):
        """Retorna todos os comentários associados a este lugar."""
        return self.comentarios.all()


class Comentario(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário em {self.lugar.nome}"


class Evento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='eventos/', null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    responsavel = models.CharField(max_length=100)
    contato = models.CharField(max_length=100, help_text='Email ou Telefone')
    curtidas = models.PositiveIntegerField(default=0)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.nome

    def is_expired(self):
        """Verifica se o evento já expirou com base na data de fim."""
        return self.data_fim < timezone.now().date()

    def save(self, *args, **kwargs):
        # Opcional: Pode impedir salvar eventos expirados diretamente
        if not self.is_expired():
            super(Evento, self).save(*args, **kwargs)
