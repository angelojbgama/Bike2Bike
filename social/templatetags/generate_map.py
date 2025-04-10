# templatetags/generate_map.py
import os
import hashlib
import json
import ast
from django import template
from django.conf import settings
from staticmap import StaticMap, Line

register = template.Library()

@register.simple_tag
def generate_static_map(bike_trajectory, post_pk, width=800, height=300, zoom=13):
    """
    Gera (ou recupera, se já existir) uma imagem PNG com o trajeto da bike.
    
    Parâmetros:
      - bike_trajectory: dados do trajeto (por exemplo, uma string que representa uma lista de dicionários)
      - post_pk: identificador do post (para gerar um nome único)
      - width, height: dimensões da imagem
      - zoom: nível de zoom (diminuir o zoom mostra uma área maior)
       
    Retorna:
      - Uma URL relativa (baseada em MEDIA_URL) para a imagem gerada.
    """
    if not bike_trajectory:
        return ""
    try:
        if isinstance(bike_trajectory, str):
            coords = ast.literal_eval(bike_trajectory)
        else:
            coords = bike_trajectory
    except Exception:
        return ""
    if not coords:
        return ""
    # Cria uma chave única para o post baseada no hash dos dados
    key_string = f"{post_pk}-{json.dumps(coords, sort_keys=True)}"
    filename_hash = hashlib.md5(key_string.encode('utf-8')).hexdigest()
    filename = f"static_maps/post_{post_pk}_{filename_hash}.png"
    full_path = os.path.join(settings.MEDIA_ROOT, filename)
    if not os.path.exists(full_path):
        try:
            m = StaticMap(width, height, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
            # Converte cada coordenada para (longitude, latitude)
            line_coords = [(pt['lng'], pt['lat']) for pt in coords]
            m.add_line(Line(line_coords, 'blue', 3))
            # Aqui, ao usar zoom=13, o mapa mostrará uma área maior
            image = m.render(zoom=zoom)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            image.save(full_path)
        except Exception as e:
            return ""
    return settings.MEDIA_URL + filename
