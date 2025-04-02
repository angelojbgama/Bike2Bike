# meu_projeto/views.py

from django.views.generic import TemplateView

# Classe que renderiza a homepage
class HomepageView(TemplateView):
    template_name = 'homepage.html'  # informa qual template HTML será renderizado
