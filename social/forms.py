# forms.py
from django import forms
from .models import Post
import json  # Para possível validação dos dados JSON

from bike2bike.mixins.DaisyUIFormMixin import DaisyUIStyledFormMixin

class NormalPostForm(DaisyUIStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        field_styles = {
            'title': {
                'classes': 'input input-bordered w-full',
                'placeholder': 'Digite o título do post'
            },
            'content': {
                'classes': 'textarea textarea-bordered',
                'placeholder': 'Digite o conteúdo do post em markdown'
            }
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content', "")
        if len(content) > 500:
            raise forms.ValidationError("O texto não pode exceder 500 caracteres.")
        
        return content

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
    # Campo oculto para armazenar os dados da trajetória (em formato JSON)
    bike_trajectory_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label="Dados do Trajeto"
    )

    class Meta:
        model = Post
        # Apenas o título será exibido para o usuário.
        # O campo bike_trajectory_data está declarado separadamente.
        fields = ["title"]
        field_styles = {
            'title': {
                'classes': 'input input-bordered w-full',
                'placeholder': 'Digite o título da rota'
            }
        }

    def clean_bike_trajectory_data(self):
        """
        Valida o campo bike_trajectory_data, garantindo que os dados sejam um JSON válido.
        """
        data = self.cleaned_data.get("bike_trajectory_data")
        if data:
            try:
                import json
                json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError("Dados do trajeto inválidos.")
        return data

