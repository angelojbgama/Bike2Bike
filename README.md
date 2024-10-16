# 🚲 Tem Bike? - Serviço de Bike-Sharing

Este projeto permite aos usuários buscar redes de **bike-sharing** por cidade e país e visualizar as **estações disponíveis em um mapa interativo**. A aplicação usa a **API CityBikes** para obter informações sobre redes e estações de bicicletas em diferentes cidades do mundo.

---

## 📋 Funcionalidades

- 🔎 **Busca por cidade e país**: Formulário para selecionar cidade e país para encontrar redes de bike-sharing.
- 🌐 **Mapa Interativo**: Exibe as estações disponíveis no mapa, utilizando **Leaflet.js**.
- 📍 **Captura de localização do usuário**: O usuário pode capturar sua posição e visualizá-la no mapa.
- 🛠️ **Requisições API**: Conecta-se à API pública CityBikes para obter informações atualizadas.
- 📦 **Detalhes das Estações**:
  - Nome da estação
  - Número de bicicletas disponíveis
  - Slots vazios
  - Endereço e localização (latitude/longitude)
  - Disponibilidade de e-bikes

---

## 📂 Estrutura do Projeto

```plaintext
tem-bike/
│
├── bike/                # Aplicação Django
│   ├── templates/
│   │   ├── bike/
│   │   │   ├── check_bike_service.html
│   │   │   └── resultados_busca.html
│   ├── forms.py         # Formulários Django
│   ├── views.py         # Views da aplicação
│   └── urls.py          # Rotas da aplicação
├── manage.py            # Arquivo principal do Django
└── README.md            # Documentação do projeto
```

---

## 🗺️ Mapas e API

Este projeto utiliza:

- **Leaflet.js**: Para exibir mapas interativos.
- **API CityBikes**: Para fornecer informações sobre redes de bike-sharing.

Links úteis:

- [Leaflet.js](https://leafletjs.com/)
- [API CityBikes](https://api.citybik.es/v2/)

---

## 📜 Documentação do Código

### 1. `get_cities_by_country(request)`
```python
def get_cities_by_country(request):
    """
    Retorna uma lista de cidades com serviços de bike-sharing para o país fornecido.
    """
    country = request.GET.get('country', None)
    if country:
        response = requests.get("http://api.citybik.es/v2/networks")
        if response.status_code == 200:
            networks = response.json().get('networks', [])
            cities = set(
                network['location']['city'] for network in networks 
                if network['location']['country'].lower() == country.lower()
            )
            return JsonResponse({'cities': list(cities)})
    return JsonResponse({'cities': []})
```

---

### 2. `BikeServiceView(FormView)`
```python
class BikeServiceView(FormView):
    """
    Renderiza o formulário de busca e redireciona para a página de resultados.
    """
    template_name = 'bike/check_bike_service.html'
    form_class = BikeSearchForm

    def form_valid(self, form):
        """
        Redireciona para a página de resultados com cidade e país na URL.
        """
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        return HttpResponseRedirect(reverse('resultados_busca', kwargs={
            'city': city,
            'country': country,
        }))
```

---

### 3. `ResultadosBuscaView(TemplateView)`
```python
class ResultadosBuscaView(TemplateView):
    """
    Exibe os resultados e detalhes das estações disponíveis.
    """
    template_name = 'bike/resultados_busca.html'

    def get_context_data(self, **kwargs):
        """
        Gera o contexto com dados de redes e estações para o template.
        """
        context = super().get_context_data(**kwargs)
        city = self.kwargs['city']
        country = self.kwargs['country']

        response = requests.get('http://api.citybik.es/v2/networks')
        if response.status_code == 200:
            networks = response.json().get('networks', [])
            bikes_data = [
                network for network in networks
                if network['location']['city'].lower() == city.lower() and
                network['location']['country'].lower() == country.lower()
            ]

            for bike in bikes_data:
                network_id = bike['id']
                network_response = requests.get(f'http://api.citybik.es/v2/networks/{network_id}')
                if network_response.status_code == 200:
                    detailed_network = network_response.json().get('network', {})
                    bike['stations'] = detailed_network.get('stations', [])
                else:
                    bike['stations'] = []

            context['bikes_data'] = bikes_data
        else:
            context['bikes_data'] = []

        stations_coordinates = []
        for bike in context['bikes_data']:
            for station in bike.get('stations', []):
                stations_coordinates.append({
                    'name': station['name'],
                    'latitude': station['latitude'],
                    'longitude': station['longitude'],
                })
        context['stations_coordinates'] = stations_coordinates

        return context
```

---

## 🛠️ Tecnologias Utilizadas

- **Python** e **Django**: Back-end.
- **HTML**, **CSS** e **Bootstrap**: Front-end responsivo.
- **Leaflet.js**: Para mapas interativos.
- **API CityBikes**: Para dados em tempo real de redes de bike-sharing.

---

## 📧 Contato

- **Email**: angelojbgama@gmail.com
- **GitHub**: [https://github.com/angelojbgama/TemBike](https://github.com/angelojbgama/TemBike)
