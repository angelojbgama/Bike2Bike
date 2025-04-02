# forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Imagens (até 5)"
    )

    class Meta:
        model = Post
        fields = ['title', 'content']  # ❌ Removido 'image' que não existe mais
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Digite um título (opcional)'}),
            'content': forms.Textarea(attrs={'placeholder': 'Escreva algo...'}),
        }

    def clean(self):
        """
        Validação personalizada: garante que pelo menos um dos campos seja preenchido.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        images = self.files.getlist('images')  # Obtém as imagens da requisição

        if not (title or content or images):
            raise forms.ValidationError("Você deve fornecer pelo menos um título, uma imagem ou um conteúdo.")

        if len(images) > 5:
            raise forms.ValidationError("Você pode enviar no máximo 5 imagens.")
        
        return cleaned_data
