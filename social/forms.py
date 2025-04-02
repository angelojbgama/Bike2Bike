# social/forms.py
from django import forms
from .models import Publicacao

class PostForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['conteudo', 'imagem']

    def clean_conteudo(self):
        conteudo = self.cleaned_data.get('conteudo', '').strip()
        if len(conteudo) < 5:
            raise forms.ValidationError("O conteúdo precisa ter ao menos 5 caracteres.")
        return conteudo
