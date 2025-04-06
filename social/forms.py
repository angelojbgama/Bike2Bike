# forms.py
from django import forms
from .models import Post
from bike2bike.mixins.DaisyUIFormMixin import DaisyUIStyledFormMixin

# forms.py

from django import forms
from django.utils.safestring import mark_safe
from bike2bike.mixins.DaisyUIFormMixin import DaisyUIStyledFormMixin
from .models import Post

# Formulário para criar um post normal (texto e imagem)
class NormalPostForm(DaisyUIStyledFormMixin, forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # Permite selecionar várias imagens
        required=False,
        label="Imagens"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "visibility"]
        field_styles = {
            'title': {
                'classes': 'input input-bordered', 
                'placeholder': 'Digite o título do post'
            },
            'content': {
                'classes': 'textarea textarea-bordered', 
                'placeholder': 'Digite o conteúdo do post em markdown'
            },
            'visibility': {
                'classes': 'select select-bordered'
            },
        }

# Formulário para criar um post em formato de carrossel
class CarouselPostForm(DaisyUIStyledFormMixin, forms.ModelForm):
    # Campo extra para upload de múltiplas imagens (do carrossel)
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Imagens do Carrossel"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "shared_link", "latitude", "longitude", "visibility"]
        field_styles = {
            'title': {'classes': 'input input-bordered', 'placeholder': 'Título curto para o carrossel'},
            'content': {'classes': 'textarea textarea-bordered', 'placeholder': 'Descrição breve'},
            'shared_link': {'classes': 'input input-bordered', 'placeholder': 'URL do link'},
            'latitude': {'classes': 'input input-bordered', 'placeholder': 'Latitude'},
            'longitude': {'classes': 'input input-bordered', 'placeholder': 'Longitude'},
            'visibility': {'classes': 'select select-bordered'},
        }

# Formulário para criar um post de enquete
class PollPostForm(DaisyUIStyledFormMixin, forms.ModelForm):
    # Campo extra para inserir as opções da enquete, separadas por vírgula
    poll_options = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "textarea textarea-bordered",
                "placeholder": "Digite as opções separadas por vírgula"
            }
        ),
        required=True,
        label="Opções da Enquete"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "shared_link", "latitude", "longitude", "visibility"]
        field_styles = {
            'title': {'classes': 'input input-bordered', 'placeholder': 'Título da enquete'},
            'content': {'classes': 'textarea textarea-bordered', 'placeholder': 'Descrição da enquete'},
            'shared_link': {'classes': 'input input-bordered', 'placeholder': 'Link opcional'},
            'latitude': {'classes': 'input input-bordered', 'placeholder': 'Latitude'},
            'longitude': {'classes': 'input input-bordered', 'placeholder': 'Longitude'},
            'visibility': {'classes': 'select select-bordered'},
        }

# Formulário para criar um post de evento
class EventPostForm(DaisyUIStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "shared_link", "latitude", "longitude", "visibility", "event_date"]
        field_styles = {
            'title': {'classes': 'input input-bordered', 'placeholder': 'Título do evento'},
            'content': {'classes': 'textarea textarea-bordered', 'placeholder': 'Descrição do evento'},
            'shared_link': {'classes': 'input input-bordered', 'placeholder': 'Link opcional'},
            'latitude': {'classes': 'input input-bordered', 'placeholder': 'Latitude'},
            'longitude': {'classes': 'input input-bordered', 'placeholder': 'Longitude'},
            'visibility': {'classes': 'select select-bordered'},
            'event_date': {'classes': 'input input-bordered', 'placeholder': 'Data e hora do evento'},
        }

# Formulário para criar um post de trajeto de bike
class BikeRoutePostForm(DaisyUIStyledFormMixin, forms.ModelForm):
    # Campo oculto que receberá os dados do trajeto em JSON, preenchido via JavaScript
    bike_trajectory_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label="Dados do Trajeto"
    )

    class Meta:
        model = Post
        fields = [
            "title", 
            "content", 
            "shared_link", 
            "latitude", 
            "longitude", 
            "visibility", 
            "bike_trajectory"
        ]
        field_styles = {
            'title': {'classes': 'input input-bordered', 'placeholder': 'Título do trajeto'},
            'content': {'classes': 'textarea textarea-bordered', 'placeholder': 'Descrição do trajeto'},
            'shared_link': {'classes': 'input input-bordered', 'placeholder': 'Link opcional'},
            'latitude': {'classes': 'input input-bordered', 'placeholder': 'Latitude'},
            'longitude': {'classes': 'input input-bordered', 'placeholder': 'Longitude'},
            'visibility': {'classes': 'select select-bordered'},
            # O campo bike_trajectory é oculto, pois os dados serão preenchidos via JS
            'bike_trajectory': {'classes': 'hidden'},
        }
