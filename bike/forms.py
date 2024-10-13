from django import forms
import requests


def get_available_cities():
    url = "http://api.citybik.es/v2/networks"
    response = requests.get(url)
    if response.status_code == 200:
        networks = response.json().get('networks', [])
        # Extraímos a lista de cidades únicas
        cities = set(network['location']['city'] for network in networks if 'city' in network['location'])
        return [(city, city) for city in sorted(cities)]
    return []

def get_available_countries():
    url = "http://api.citybik.es/v2/networks"
    response = requests.get(url)
    if response.status_code == 200:
        networks = response.json().get('networks', [])
        # Extraímos a lista de países únicos
        countries = set(network['location']['country'] for network in networks if 'country' in network['location'])
        return [(country, country) for country in sorted(countries)]
    return []

class BikeSearchForm(forms.Form):
    city = forms.ChoiceField(label='Cidade', choices=[])
    country = forms.ChoiceField(label='País', choices=[])

    def __init__(self, *args, **kwargs):
        super(BikeSearchForm, self).__init__(*args, **kwargs)
        # Preenche as listas de cidades e países dinamicamente
        self.fields['city'].choices = get_available_cities()
        self.fields['country'].choices = get_available_countries()
