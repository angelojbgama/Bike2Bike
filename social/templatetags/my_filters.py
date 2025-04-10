import json
import ast
from django import template

register = template.Library()

@register.filter(name='to_json')
def to_json(value):
    """
    Converte o valor, que pode ser uma string contendo uma lista de dicionários com aspas simples,
    em um JSON válido (com aspas duplas) usando ast.literal_eval e json.dumps.
    """
    try:
        if isinstance(value, str):
            parsed = ast.literal_eval(value)
        else:
            parsed = value
        return json.dumps(parsed)
    except Exception as e:
        return value

@register.filter(name="osm_static_map")
def osm_static_map(json_string, size="600x300"):
    """
    Recebe uma string JSON (resultado do filtro to_json) que representa uma lista de dicionários
    com chaves 'lat' e 'lng' e gera uma URL para uma imagem estática que exibe o trajeto.
    
    Exemplo de URL gerada:
    https://staticmap.openstreetmap.de/staticmap.php?size=600x300&center=-22.81472,-43.24635&zoom=14&path=color:0x0000ff|weight:3|-22.81472,-43.24635|-22.81477,-43.24625|...
    """
    try:
        coords = json.loads(json_string)
        if not coords:
            return ""
        # Cria o parâmetro 'path'; veja que separamos os pontos por "|"
        path_param = "path=color:0x0000ff|weight:3|"
        points = []
        for pt in coords:
            points.append(f"{pt['lat']},{pt['lng']}")
        path_param += "|".join(points)
        # Para centralizar, usamos o primeiro ponto e forçamos um zoom fixo (ex.: 14)
        center = coords[0]
        center_param = f"center={center['lat']},{center['lng']}"
        base_url = "https://staticmap.openstreetmap.de/staticmap.php"
        # Note que adicionamos &zoom=14 para definir a escala do mapa
        url = f"{base_url}?size={size}&{center_param}&zoom=14&{path_param}"
        return url
    except Exception:
        return ""
