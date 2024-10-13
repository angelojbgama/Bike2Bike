from django.urls import path
from .views import BikeServiceView, ResultadosBuscaView, get_cities_by_country

urlpatterns = [
    path('', BikeServiceView.as_view(), name='check_bike_service'),
    path('resultados/<str:city>/<str:country>/', ResultadosBuscaView.as_view(), name='resultados_busca'),
    path('get-cities/', get_cities_by_country, name='get_cities_by_country'),
]
