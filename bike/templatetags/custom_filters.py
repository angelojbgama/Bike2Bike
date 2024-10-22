from django import template

register = template.Library()

@register.filter(name='star_range')
def star_range(start, end):
    """Gera um range entre start e end."""
    return range(start, end + 1)

@register.filter(name='multiply_star')
def multiply_star(value):
    """Retorna uma string com N estrelas."""
    return '⭐' * value
