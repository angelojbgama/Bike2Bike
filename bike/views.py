from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, FormView
from django.http import JsonResponse, HttpResponseRedirect
from .models import Lugar, Comentario, AvaliacaoComentario
from .forms import BikeSearchForm
import requests
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # Para desabilitar CSRF se necessário
from django.db.models import Avg, Sum




@csrf_exempt
@require_POST
def salvar_avaliacao(request, comentario_id):
    """
    Adiciona uma nova avaliação a um comentário existente e retorna a soma e média das avaliações.
    """
    try:
        estrelas = int(request.POST.get('estrelas'))
        comentario = get_object_or_404(Comentario, pk=comentario_id)

        # Cria uma nova avaliação para o comentário
        AvaliacaoComentario.objects.create(comentario=comentario, estrelas=estrelas)

        # Recalcular média e soma das avaliações do comentário
        avaliacoes = comentario.avaliacoes.all()
        media_estrelas = avaliacoes.aggregate(Avg('estrelas'))['estrelas__avg']
        soma_estrelas = avaliacoes.aggregate(Sum('estrelas'))['estrelas__sum']

        return JsonResponse({
            'status': 'success',
            'estrelas': estrelas,
            'media_estrelas': round(media_estrelas, 2) if media_estrelas else 0,
            'soma_estrelas': soma_estrelas or 0
        })

    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Valor inválido'}, status=400)



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
    """
    Renderiza e processa o formulário de busca de bike-sharing.
    """
    template_name = "bike/check_bike_service.html"
    form_class = BikeSearchForm

    def form_valid(self, form):
        """
        Redireciona para resultados após validação do formulário.
        """
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
    """
    Exibe resultados de serviços de bike-sharing para cidade e país específicos.
    """
    template_name = "bike/resultados_busca.html"

    def get_context_data(self, **kwargs):
        """
        Obtém dados de contexto para a página de resultados.
        """
        context = super().get_context_data(**kwargs)
        city = self.kwargs["city"]
        country = self.kwargs["country"]

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

        lugares = Lugar.objects.all()
        lugares_data = [
            {
                "nome": lugar.nome,
                "descricao": lugar.descricao,
                "latitude": lugar.latitude,
                "longitude": lugar.longitude,
                "tipo": lugar.get_tipo_display(),
                "media_estrelas": lugar.media_estrelas(),  # Adiciona a média das estrelas
                "comentarios_url": reverse("comentario_lugar_list", args=[lugar.id]),
            }
            for lugar in lugares
        ]
        context["lugares_data"] = lugares_data

        context["city"] = city
        context["country"] = country
        return context


class LugarCreateView(CreateView):
    """
    Cria um novo lugar no banco de dados.
    """
    model = Lugar
    fields = ["nome", "descricao", "latitude", "longitude", "tipo"]
    template_name = "bike/cadastrar_lugar.html"
    success_url = reverse_lazy("check_bike_service")


class SobreServicoView(TemplateView):
    """
    Exibe a página inicial sobre o serviço.
    """
    template_name = "bike/home.html"


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
        context["media_estrelas"] = lugar.media_estrelas()
        context["soma_estrelas"] = lugar.soma_estrelas()

        # Adiciona a soma e média de avaliações para cada comentário
        for comentario in context["comentarios"]:
            comentario.soma_estrelas = comentario.avaliacoes.aggregate(Sum('estrelas'))['estrelas__sum'] or 0
            comentario.media_estrelas = comentario.avaliacoes.aggregate(Avg('estrelas'))['estrelas__avg'] or 0

        return context



class ComentarioCreateView(CreateView):
    """
    Cria um novo comentário para um lugar.
    """
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

from django.shortcuts import get_object_or_404, redirect

class ComentarioUpdateView(UpdateView):
    model = Comentario
    fields = ["estrelas"]  # Atualizamos apenas as estrelas
    template_name = "bike/comentarios/comentario_form.html"

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('comentario_lugar_list', kwargs={'lugar_id': self.object.lugar_id}))

class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = "bike/comentarios/comentario_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lugar_id'] = self.object.lugar_id  # Certifique-se de que lugar_id está disponível
        return context

    def get_success_url(self):
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": self.object.lugar_id})


class ComentarioUpdateEstrelasView(UpdateView):
    model = Comentario
    fields = ["estrelas"]
    template_name = "bike/comentarios/comentario_update_estrelas.html"

    def get_success_url(self):
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": self.object.lugar_id})
