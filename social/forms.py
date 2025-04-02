# social/forms.py
from django import forms
from .models import Publicacao

class PostForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['conteudo', 'imagem']  # nomes em português, iguais aos da model
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'O que você está pensando?'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered'
            }),
        }
