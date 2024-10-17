from django.urls import path
from .views import BikeServiceView, ResultadosBuscaView, get_cities_by_country, LugarCreateView

urlpatterns = [
    path('', BikeServiceView.as_view(), name='check_bike_service'),
    path('resultados/<str:city>/<str:country>/', ResultadosBuscaView.as_view(), name='resultados_busca'),
    path('cadastrar/', LugarCreateView.as_view(), name='cadastrar_lugar'),
    
    
    path('get-cities/', get_cities_by_country, name='get_cities_by_country'),

]
