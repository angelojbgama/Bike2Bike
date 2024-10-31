from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, FormView, DetailView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from .models import Lugar, Comentario, Evento
from .forms import BikeSearchForm, EventoForm
import requests
from django.db.models import Q
import math
from django.utils import timezone

def get_cities_by_country(request):
    """
    Retorna cidades disponíveis para um país usando a API CityBikes.
    """
    country = request.GET.get("country", None)
    if country:
        url = "http://api.citybik.es/v2/networks"
        response = requests.get(url)
        if response.status_code == 200:
            networks = response.json().get("networks", [])
            cities = set(
                network["location"]["city"]
                for network in networks
                if network["location"]["country"].lower() == country.lower()
            )
            return JsonResponse({"cities": list(cities)})
    return JsonResponse({"cities": []})

class BikeServiceView(FormView):
    template_name = "bike/check_bike_service.html"
    form_class = BikeSearchForm

    def form_valid(self, form):
        city = form.cleaned_data["city"]
        country = form.cleaned_data["country"]
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
    template_name = "bike/resultados_busca.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.kwargs["city"]
        country = self.kwargs["country"]

        # Dados das redes de bicicleta
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
                bike["stations"] = network_response.json().get("network", {}).get("stations", []) if network_response.status_code == 200 else []

            context["bikes_data"] = bikes_data
        else:
            context["bikes_data"] = []

        # Dados dos lugares
        lugares = Lugar.objects.all()
        lugares_data = [
            {
                "nome": lugar.nome,
                "descricao": lugar.descricao,
                "latitude": lugar.latitude,
                "longitude": lugar.longitude,
                "tipo": lugar.get_tipo_display(),
                "comentarios_url": reverse("comentario_lugar_list", args=[lugar.id]),
            }
            for lugar in lugares
        ]
        context["lugares_data"] = lugares_data

        # Dados dos eventos válidos e com coordenadas preenchidas
        eventos = Evento.objects.filter(
            data_fim__gte=timezone.now().date(), latitude__isnull=False, longitude__isnull=False
        )
        eventos_data = [
            {
                "nome": evento.nome,
                "descricao": evento.descricao,
                "latitude": evento.latitude,
                "longitude": evento.longitude,
                "curtidas": evento.curtidas,
                "data_inicio": evento.data_inicio.strftime("%Y-%m-%d"),
                "data_fim": evento.data_fim.strftime("%Y-%m-%d"),  # Formata a data para JSON
                "contato": evento.contato,
                "detalhes_url": reverse("evento_detalhes", args=[evento.pk])  # Aqui garantimos que estamos acessando o ID de um único objeto

            }
            for evento in eventos
        ]
        context["eventos_data"] = eventos_data

        context["city"] = city
        context["country"] = country
        return context



class LugarCreateView(CreateView):
    model = Lugar
    fields = ["nome", "descricao", "latitude", "longitude", "tipo"]
    template_name = "bike/cadastrar_lugar.html"
    success_url = reverse_lazy("check_bike_service")

class ComentarioLugarListView(ListView):
    model = Comentario
    template_name = "bike/comentarios/comentario_lugar_list.html"
    context_object_name = "comentarios"

    def get_queryset(self):
        lugar_id = self.kwargs.get("lugar_id")
        return Comentario.objects.filter(lugar_id=lugar_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lugar = Lugar.objects.get(id=self.kwargs.get("lugar_id"))
        context["lugar"] = lugar
        return context

class ComentarioCreateView(CreateView):
    model = Comentario
    fields = ["texto"]
    template_name = "bike/comentarios/comentario_form.html"

    def form_valid(self, form):
        lugar_id = self.kwargs["lugar_id"]
        form.instance.lugar_id = lugar_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lugar_id"] = self.kwargs["lugar_id"]
        return context

    def get_success_url(self):
        lugar_id = self.kwargs["lugar_id"]
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": lugar_id})

class ComentarioUpdateView(UpdateView):
    model = Comentario
    fields = ["texto"]  # Atualizamos apenas o texto do comentário
    template_name = "bike/comentarios/comentario_form.html"

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('comentario_lugar_list', kwargs={'lugar_id': self.object.lugar_id}))

class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = "bike/comentarios/comentario_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lugar_id'] = self.object.lugar_id
        return context

    def get_success_url(self):
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": self.object.lugar_id})

class SobreServicoView(TemplateView):
    """
    Exibe a página inicial sobre o serviço com informações adicionais.
    """
    template_name = "bike/home.html"

    def get_context_data(self, **kwargs):
        """
        Adiciona dados dinâmicos ao contexto da página.
        """
        context = super().get_context_data(**kwargs)
        context["nome_servico"] = "Bike Sharing Service"
        context["descricao_servico"] = (
            "Nosso serviço conecta você às melhores opções de bike-sharing em todo o mundo."
        )
        context["email_contato"] = "contato@bikeservice.com"
        return context


class RotaView(TemplateView):
    """
    View para exibir o mapa e calcular rotas entre dois pontos.
    """
    template_name = "bike/rota.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Exemplos de coordenadas iniciais (opcional)
        context["start_lat"] = -23.55052  # São Paulo (Latitude)
        context["start_lon"] = -46.6333  # São Paulo (Longitude)
        return context



class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'bike/eventos/evento_form.html'
    success_url = reverse_lazy('eventos-list')

class EventoListView(ListView):
    model = Evento
    template_name = 'bike/eventos/evento_list.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        queryset = super().get_queryset()
        latitude = self.request.GET.get('latitude')
        longitude = self.request.GET.get('longitude')
        raio = self.request.GET.get('raio')

        if latitude and longitude and raio:
            try:
                lat = float(latitude)
                lon = float(longitude)
                raio_km = float(raio)

                # Convertendo o raio de km para metros
                raio_m = raio_km * 1000

                # Calcula a distância entre dois pontos usando a fórmula de Haversine
                def haversine(lat1, lon1, lat2, lon2):
                    R = 6371000  # Raio da Terra em metros
                    phi1 = math.radians(lat1)
                    phi2 = math.radians(lat2)
                    delta_phi = math.radians(lat2 - lat1)
                    delta_lambda = math.radians(lon2 - lon1)

                    a = math.sin(delta_phi / 2) ** 2 + \
                        math.cos(phi1) * math.cos(phi2) * \
                        math.sin(delta_lambda / 2) ** 2

                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

                    return R * c  # Retorna a distância em metros

                # Filtrar eventos próximos
                eventos_proximos = []
                for evento in queryset:
                    distancia = haversine(lat, lon, evento.latitude, evento.longitude)
                    if distancia <= raio_m:
                        eventos_proximos.append(evento.id)

                queryset = queryset.filter(id__in=eventos_proximos)

            except ValueError:
                # Se latitude, longitude ou raio não forem números válidos, retorna a queryset padrão
                pass

        return queryset



class EventoDetailView(DetailView):
    model = Evento
    template_name = 'bike/eventos/evento_detail.html'


    def post(self, request, *args, **kwargs):
        evento = self.get_object()
        evento.curtidas += 1
        evento.save()
        return self.get(request, *args, **kwargs)
