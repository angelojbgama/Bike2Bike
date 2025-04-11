import os
import hashlib
import json
import ast
import math
from django import template
from django.conf import settings
from staticmap import StaticMap, Line

register = template.Library()

# Função auxiliar para converter latitude em radianos no contexto da projeção de Mercator.
def lat_rad(lat):
    """
    Converte uma latitude (em graus) para o valor em radianos da projeção de Mercator.
    """
    # Calcula o seno da latitude convertida para radianos
    sin_lat = math.sin(math.radians(lat))
    # Aplica a fórmula de transformação para Mercator
    rad = math.log((1 + sin_lat) / (1 - sin_lat)) / 2
    return rad

# Função que calcula o zoom ideal baseado na área que os pontos cobrem (bounding box) e nas dimensões da imagem.
def calculate_optimal_zoom(min_lat, max_lat, min_lng, max_lng, map_width, map_height):
    """
    Calcula o nível de zoom ideal para enquadrar um conjunto de coordenadas em uma imagem de mapa.
    
    Parâmetros:
      - min_lat, max_lat: latitude mínima e máxima do conjunto de pontos.
      - min_lng, max_lng: longitude mínima e máxima do conjunto de pontos.
      - map_width, map_height: dimensões da imagem do mapa em pixels.
      
    Retorna:
      - Um valor inteiro de zoom que melhor se ajusta ao conjunto de coordenadas.
    """
    tile_size = 256  # Tamanho padrão do tile em pixels
    # Calcula a fração do mapa que as latitudes ocupam, usando a projeção Mercator
    lat_fraction = (lat_rad(max_lat) - lat_rad(min_lat)) / math.pi
    # A fração longitudinal é a proporção da distância em relação a 360°
    lng_fraction = (max_lng - min_lng) / 360

    # Calcula o nível de zoom necessário para as dimensões verticais e horizontais
    # math.log2 calcula logaritmo na base 2, que é usado para determinar o nível de zoom
    zoom_lat = math.log2(map_height / tile_size / lat_fraction) if lat_fraction > 0 else float('inf')
    zoom_lng = math.log2(map_width / tile_size / lng_fraction) if lng_fraction > 0 else float('inf')
    
    # O zoom ideal é o mínimo dos dois, para garantir que os pontos caberão na imagem
    optimal_zoom = int(min(zoom_lat, zoom_lng))
    # Garante que o zoom não seja negativo
    if optimal_zoom < 0:
        optimal_zoom = 0
    return optimal_zoom

@register.simple_tag
def generate_static_map(bike_trajectory, post_pk, width=800, height=300, zoom=None):
    """
    Gera (ou recupera, se já existir) uma imagem PNG com o trajeto da bike.
    
    Parâmetros:
      - bike_trajectory: dados do trajeto (por exemplo, uma string ou lista de dicionários com 'lat' e 'lng')
      - post_pk: identificador do post (usado para gerar um nome único para a imagem)
      - width, height: dimensões da imagem do mapa em pixels
      - zoom: nível de zoom. Se não for informado, é calculado automaticamente para abranger todas as coordenadas
      
    Retorna:
      - Uma URL relativa (baseada em MEDIA_URL) para a imagem gerada.
    """
    if not bike_trajectory:
        return ""
    try:
        # Se os dados do trajeto estiverem em forma de string, converte para uma lista de dicionários
        if isinstance(bike_trajectory, str):
            coords = ast.literal_eval(bike_trajectory)
        else:
            coords = bike_trajectory
    except Exception:
        return ""
    if not coords:
        return ""
    
    # Se o zoom não for informado, calculamos o zoom ideal automaticamente
    if zoom is None:
        # Extraímos todas as latitudes e longitudes válidas dos pontos
        lats = [pt['lat'] for pt in coords if 'lat' in pt and 'lng' in pt]
        lngs = [pt['lng'] for pt in coords if 'lat' in pt and 'lng' in pt]
        if lats and lngs:
            min_lat, max_lat = min(lats), max(lats)
            min_lng, max_lng = min(lngs), max(lngs)
            # Calcula o zoom ideal com base na função auxiliar
            zoom = calculate_optimal_zoom(min_lat, max_lat, min_lng, max_lng, width, height)
        else:
            # Se houver problema nas coordenadas, usa um zoom padrão
            zoom = 13

    # Cria uma chave única para o post baseada no hash dos dados do trajeto e dos parâmetros de renderização
    key_string = f"{post_pk}-{json.dumps(coords, sort_keys=True)}-{width}-{height}-{zoom}"
    filename_hash = hashlib.md5(key_string.encode('utf-8')).hexdigest()
    filename = f"static_maps/post_{post_pk}_{filename_hash}.png"
    full_path = os.path.join(settings.MEDIA_ROOT, filename)
    
    # Se a imagem ainda não foi gerada, cria o mapa usando a biblioteca StaticMap
    if not os.path.exists(full_path):
        try:
            # Cria o objeto do mapa com as dimensões especificadas e usando um template de URL para os tiles
            m = StaticMap(width, height, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
            # Converte cada ponto para uma tupla (longitude, latitude) e adiciona uma linha azul que representa o trajeto
            line_coords = [(pt['lng'], pt['lat']) for pt in coords if 'lat' in pt and 'lng' in pt]
            m.add_line(Line(line_coords, 'blue', 3))
            # Renderiza o mapa com o nível de zoom calculado ou informado
            image = m.render(zoom=zoom)
            # Garante que o diretório de destino exista e salva a imagem
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            image.save(full_path)
        except Exception as e:
            # Em caso de erro, retorna uma string vazia
            return ""
    # Retorna a URL da imagem usando MEDIA_URL
    return settings.MEDIA_URL + filename
