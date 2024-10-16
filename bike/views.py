from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .forms import BikeSearchForm
import requests

def get_cities_by_country(request):
    """
    View que busca cidades disponíveis para um país específico usando a API CityBikes.

    Parâmetros:
    - request: HttpRequest contendo a querystring com o nome do país.

    Funcionamento:
    - Se o parâmetro 'country' estiver presente na querystring, a função faz uma requisição
      para a API CityBikes e retorna uma lista de cidades que possuem serviços de bike-sharing
      no país especificado.
    - Caso o país não seja encontrado ou a API falhe, retorna uma lista vazia de cidades.

    Retorno:
    - JsonResponse: Dicionário com a lista de cidades encontradas.
    """

    country = request.GET.get('country', None)  # Obtém o país da querystring.
    if country:
        url = "http://api.citybik.es/v2/networks"
        response = requests.get(url)
        if response.status_code == 200:
            networks = response.json().get('networks', [])
            # Filtra as cidades com base no país fornecido.
            cities = set(
                network['location']['city'] for network in networks 
                if network['location']['country'].lower() == country.lower()
            )
            return JsonResponse({'cities': list(cities)})  # Retorna as cidades encontradas.
    return JsonResponse({'cities': []})  # Caso não haja correspondências, retorna lista vazia.


class BikeServiceView(FormView):
    """
    View responsável por renderizar e processar o formulário de busca de serviços de bike-sharing.

    Herda:
    - FormView: View baseada em formulário do Django.

    Atributos:
    - template_name: Template HTML utilizado para exibir o formulário.
    - form_class: Classe do formulário associada a essa view.

    Funcionamento:
    - Se o formulário for válido, o método form_valid é chamado, e o usuário é redirecionado
      para a página de resultados, passando os dados de cidade e país como parâmetros na URL.
    """

    template_name = 'bike/check_bike_service.html'
    form_class = BikeSearchForm

    def form_valid(self, form):
        """
        Processa o formulário após sua validação.

        Parâmetros:
        - form: Instância do formulário validado.

        Retorno:
        - HttpResponseRedirect: Redireciona para a página de resultados com cidade e país
          como parâmetros na URL.
        """
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        
        # Redireciona para a view de resultados com os dados do formulário na URL.
        return HttpResponseRedirect(reverse('resultados_busca', kwargs={
            'city': city,
            'country': country,
        }))


class ResultadosBuscaView(TemplateView):
    """
    View responsável por exibir os resultados dos serviços de bike-sharing para uma cidade e país específicos.

    Herda:
    - TemplateView: View baseada em template do Django.

    Atributos:
    - template_name: Template HTML usado para exibir os resultados.

    Funcionamento:
    - Busca todas as redes de bike-sharing disponíveis usando a API CityBikes.
    - Filtra as redes com base na cidade e país fornecidos.
    - Para cada rede encontrada, faz uma requisição adicional para buscar os detalhes das estações.
    - Prepara os dados para serem exibidos na página e adiciona coordenadas das estações para exibir no mapa.
    """

    template_name = 'bike/resultados_busca.html'

    def get_context_data(self, **kwargs):
        """
        Gera o contexto para renderizar o template com os dados dos serviços de bike-sharing.

        Parâmetros:
        - kwargs: Parâmetros adicionais, incluindo cidade e país.

        Retorno:
        - context: Dicionário com dados para serem usados no template.
        """
        context = super().get_context_data(**kwargs)
        city = self.kwargs['city']
        country = self.kwargs['country']

        # Faz requisição à API CityBikes para obter todas as redes.
        response = requests.get('http://api.citybik.es/v2/networks')
        if response.status_code == 200:
            networks = response.json().get('networks', [])
            # Filtra as redes que correspondem à cidade e ao país fornecidos.
            bikes_data = [
                network for network in networks
                if network['location']['city'].lower() == city.lower() and
                network['location']['country'].lower() == country.lower()
            ]

            # Para cada rede encontrada, faz uma requisição adicional para obter detalhes das estações.
            for bike in bikes_data:
                network_id = bike['id']
                network_response = requests.get(f'http://api.citybik.es/v2/networks/{network_id}')
                if network_response.status_code == 200:
                    detailed_network = network_response.json().get('network', {})
                    bike['stations'] = detailed_network.get('stations', [])  # Adiciona estações ao bike.
                else:
                    bike['stations'] = []  # Se falhar, define lista vazia de estações.

            context['bikes_data'] = bikes_data  # Adiciona dados de bikes ao contexto.
        else:
            context['bikes_data'] = []  # Caso a requisição falhe, define lista vazia.

        context['city'] = city  # Adiciona cidade ao contexto.
        context['country'] = country  # Adiciona país ao contexto.

        # Coleta coordenadas das estações para exibir no mapa.
        stations_coordinates = []
        for bike in context['bikes_data']:
            for station in bike.get('stations', []):
                stations_coordinates.append({
                    'name': station['name'],
                    'latitude': station['latitude'],
                    'longitude': station['longitude'],
                })
        context['stations_coordinates'] = stations_coordinates  # Adiciona coordenadas ao contexto.

        return context  # Retorna o contexto para renderizar o template.
