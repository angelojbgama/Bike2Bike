# social/templatetags/markdown_extras.py

import markdown  # Importa a biblioteca para conversão de Markdown em HTML
from django import template

register = template.Library()  # Registra os filtros do Django

@register.filter(name='markdown')
def markdown_format(text):
    """
    Converte o texto em Markdown para HTML, utilizando as extensões:
    - extra: adiciona funcionalidades extras ao Markdown
    - fenced_code: permite blocos de código com crases triplas
    - codehilite: adiciona destaque de sintaxe para blocos de código
    """
    return markdown.markdown(text, extensions=['extra', 'fenced_code', 'codehilite'])
