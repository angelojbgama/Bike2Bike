from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import BikeSearchForm
import requests
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
import requests


def get_cities_by_country(request):
    country = request.GET.get('country', None)
    if country:
        url = "http://api.citybik.es/v2/networks"
        response = requests.get(url)
        if response.status_code == 200:
            networks = response.json().get('networks', [])
            # Filtramos as cidades com base no país selecionado
            cities = set(
                network['location']['city'] for network in networks 
                if network['location']['country'].lower() == country.lower()
            )
            return JsonResponse({'cities': list(cities)})
    return JsonResponse({'cities': []})


class BikeServiceView(FormView):
    template_name = 'bike/check_bike_service.html'
    form_class = BikeSearchForm

    def form_valid(self, form):
        # Captura os dados do formulário
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        
        # Redireciona para a página de resultados, passando a cidade e o país como parâmetros
        return HttpResponseRedirect(reverse('resultados_busca', kwargs={
            'city': city,
            'country': country,
        }))


class ResultadosBuscaView(TemplateView):
    template_name = 'bike/resultados_busca.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.kwargs['city']
        country = self.kwargs['country']

        # Fazer requisição à API para buscar as redes na cidade e país selecionados
        response = requests.get('http://api.citybik.es/v2/networks')
        if response.status_code == 200:
            networks = response.json().get('networks', [])
            bikes_data = [
                network for network in networks
                if network['location']['city'].lower() == city.lower() and
                network['location']['country'].lower() == country.lower()
            ]
            context['bikes_data'] = bikes_data
        else:
            context['bikes_data'] = []
        context['city'] = city
        context['country'] = country
        return context
