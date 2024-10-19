from .models import Lugar

from .forms import BikeSearchForm

from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, CreateView
from django.http import JsonResponse, HttpResponseRedirect

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

    country = request.GET.get("country", None)  # Obtém o país da querystring.
    if country:
        url = "http://api.citybik.es/v2/networks"
        response = requests.get(url)
        if response.status_code == 200:
            networks = response.json().get("networks", [])
            # Filtra as cidades com base no país fornecido.
            cities = set(
                network["location"]["city"]
                for network in networks
                if network["location"]["country"].lower() == country.lower()
            )
            return JsonResponse(
                {"cities": list(cities)}
            )  # Retorna as cidades encontradas.
    return JsonResponse(
        {"cities": []}
    )  # Caso não haja correspondências, retorna lista vazia.


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

    template_name = "bike/check_bike_service.html"
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
        city = form.cleaned_data["city"]
        country = form.cleaned_data["country"]

        # Redireciona para a view de resultados com os dados do formulário na URL.
        return HttpResponseRedirect(
            reverse(
                "resultados_busca",
                kwargs={
                    "city": city,
                    "country": country,
                },
            )
        )


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

    template_name = "bike/resultados_busca.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.kwargs["city"]
        country = self.kwargs["country"]

        # Faz requisição à API CityBikes
        response = requests.get("http://api.citybik.es/v2/networks")
        if response.status_code == 200:
            networks = response.json().get("networks", [])
            bikes_data = [
                network
                for network in networks
                if network["location"]["city"].lower() == city.lower()
                and network["location"]["country"].lower() == country.lower()
            ]

            for bike in bikes_data:
                network_id = bike["id"]
                network_response = requests.get(
                    f"http://api.citybik.es/v2/networks/{network_id}"
                )
                if network_response.status_code == 200:
                    bike["stations"] = (
                        network_response.json().get("network", {}).get("stations", [])
                    )
                else:
                    bike["stations"] = []

            context["bikes_data"] = bikes_data
        else:
            context["bikes_data"] = []

        # Adiciona lugares do banco de dados ao contexto
        lugares = Lugar.objects.all()
        lugares_data = [
            {
                "nome": lugar.nome,
                "descricao": lugar.descricao,
                "latitude": lugar.latitude,
                "longitude": lugar.longitude,
                "tipo": lugar.get_tipo_display(),
            }
            for lugar in lugares
        ]
        context["lugares_data"] = lugares_data

        context["city"] = city
        context["country"] = country
        return context


class LugarCreateView(CreateView):
    model = Lugar
    fields = ["nome", "descricao", "latitude", "longitude", "tipo"]
    template_name = "bike/cadastrar_lugar.html"
    success_url = reverse_lazy("check_bike_service")  # Redireciona após o cadastro
