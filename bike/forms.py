from django import forms
from .models import Lugar, Comentario
import requests

# Dicionário para mapear códigos de países para seus nomes em português
COUNTRY_NAME_MAPPING = {
    "AF": "Afeganistão",
    "AL": "Albânia",
    "DZ": "Argélia",
    "AS": "Samoa Americana",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antártida",
    "AG": "Antígua e Barbuda",
    "AR": "Argentina",
    "AM": "Armênia",
    "AW": "Aruba",
    "AU": "Austrália",
    "AT": "Áustria",
    "AZ": "Azerbaijão",
    "BS": "Bahamas",
    "BH": "Bahrein",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Bielorrússia",
    "BE": "Bélgica",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermudas",
    "BT": "Butão",
    "BO": "Bolívia",
    "BA": "Bósnia e Herzegovina",
    "BW": "Botswana",
    "BR": "Brasil",
    "BN": "Brunei",
    "BG": "Bulgária",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "CV": "Cabo Verde",
    "KH": "Camboja",
    "CM": "Camarões",
    "CA": "Canadá",
    "KY": "Ilhas Cayman",
    "CF": "República Centro-Africana",
    "TD": "Chade",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colômbia",
    "KM": "Comores",
    "CG": "Congo",
    "CD": "Congo (República Democrática)",
    "CR": "Costa Rica",
    "CI": "Costa do Marfim",
    "HR": "Croácia",
    "CU": "Cuba",
    "CY": "Chipre",
    "CZ": "República Tcheca",
    "DK": "Dinamarca",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "República Dominicana",
    "EC": "Equador",
    "EG": "Egito",
    "SV": "El Salvador",
    "GQ": "Guiné Equatorial",
    "ER": "Eritreia",
    "EE": "Estônia",
    "SZ": "Eswatini",
    "ET": "Etiópia",
    "FJ": "Fiji",
    "FI": "Finlândia",
    "FR": "França",
    "GA": "Gabão",
    "GM": "Gâmbia",
    "GE": "Geórgia",
    "DE": "Alemanha",
    "GH": "Gana",
    "GR": "Grécia",
    "GD": "Granada",
    "GT": "Guatemala",
    "GN": "Guiné",
    "GW": "Guiné-Bissau",
    "GY": "Guiana",
    "HT": "Haiti",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungria",
    "IS": "Islândia",
    "IN": "Índia",
    "ID": "Indonésia",
    "IR": "Irã",
    "IQ": "Iraque",
    "IE": "Irlanda",
    "IL": "Israel",
    "IT": "Itália",
    "JM": "Jamaica",
    "JP": "Japão",
    "JO": "Jordânia",
    "KZ": "Cazaquistão",
    "KE": "Quênia",
    "KI": "Kiribati",
    "KW": "Kuwait",
    "KG": "Quirguistão",
    "LA": "Laos",
    "LV": "Letônia",
    "LB": "Líbano",
    "LS": "Lesoto",
    "LR": "Libéria",
    "LY": "Líbia",
    "LI": "Liechtenstein",
    "LT": "Lituânia",
    "LU": "Luxemburgo",
    "MO": "Macau",
    "MG": "Madagáscar",
    "MW": "Malawi",
    "MY": "Malásia",
    "MV": "Maldivas",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Ilhas Marshall",
    "MR": "Mauritânia",
    "MU": "Maurício",
    "MX": "México",
    "FM": "Micronésia",
    "MD": "Moldova",
    "MC": "Mônaco",
    "MN": "Mongólia",
    "ME": "Montenegro",
    "MA": "Marrocos",
    "MZ": "Moçambique",
    "MM": "Mianmar",
    "NA": "Namíbia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Países Baixos",
    "NZ": "Nova Zelândia",
    "NI": "Nicarágua",
    "NE": "Níger",
    "NG": "Nigéria",
    "KP": "Coreia do Norte",
    "NO": "Noruega",
    "OM": "Omã",
    "PK": "Paquistão",
    "PW": "Palau",
    "PA": "Panamá",
    "PG": "Papua-Nova Guiné",
    "PY": "Paraguai",
    "PE": "Peru",
    "PH": "Filipinas",
    "PL": "Polônia",
    "PT": "Portugal",
    "QA": "Catar",
    "RO": "Romênia",
    "RU": "Rússia",
    "RW": "Ruanda",
    "KN": "São Cristóvão e Nevis",
    "LC": "Santa Lúcia",
    "VC": "São Vicente e Granadinas",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "São Tomé e Príncipe",
    "SA": "Arábia Saudita",
    "SN": "Senegal",
    "RS": "Sérvia",
    "SC": "Seychelles",
    "SL": "Serra Leoa",
    "SG": "Singapura",
    "SK": "Eslováquia",
    "SI": "Eslovênia",
    "SB": "Ilhas Salomão",
    "SO": "Somália",
    "ZA": "África do Sul",
    "KR": "Coreia do Sul",
    "SS": "Sudão do Sul",
    "ES": "Espanha",
    "LK": "Sri Lanka",
    "SD": "Sudão",
    "SR": "Suriname",
    "SE": "Suécia",
    "CH": "Suíça",
    "SY": "Síria",
    "TW": "Taiwan",
    "TJ": "Tadjiquistão",
    "TZ": "Tanzânia",
    "TH": "Tailândia",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TO": "Tonga",
    "TT": "Trinidad e Tobago",
    "TN": "Tunísia",
    "TR": "Turquia",
    "TM": "Turcomenistão",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ucrânia",
    "AE": "Emirados Árabes Unidos",
    "GB": "Reino Unido",
    "US": "Estados Unidos",
    "UY": "Uruguai",
    "UZ": "Uzbequistão",
    "VU": "Vanuatu",
    "VA": "Vaticano",
    "VE": "Venezuela",
    "VN": "Vietnã",
    "YE": "Iêmen",
    "ZM": "Zâmbia",
    "ZW": "Zimbábue"
}


def get_available_cities():
    url = "http://api.citybik.es/v2/networks"
    response = requests.get(url)
    if response.status_code == 200:
        networks = response.json().get('networks', [])
        cities = set(network['location']['city'] for network in networks if 'city' in network['location'])
        return [(city, city) for city in sorted(cities)]
    return []

def get_available_countries():
    url = "http://api.citybik.es/v2/networks"
    response = requests.get(url)
    if response.status_code == 200:
        networks = response.json().get('networks', [])
        countries = set(network['location']['country'] for network in networks if 'country' in network['location'])
        country_choices = []
        for country in sorted(countries):
            country_name = COUNTRY_NAME_MAPPING.get(country, country)
            country_choices.append((country, country_name))
        return country_choices
    return []

class BikeSearchForm(forms.Form):
    city = forms.ChoiceField(
        label='Cidade',
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select mb-3',
            'id': 'id_city'
        })
    )
    country = forms.ChoiceField(
        label='País',
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select mb-3',
            'id': 'id_country'
        })
    )

    def __init__(self, *args, **kwargs):
        super(BikeSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices = get_available_cities()
        self.fields['country'].choices = get_available_countries()

class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ['nome', 'descricao', 'latitude', 'longitude', 'tipo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class ComentarioForm(forms.ModelForm):
    """
    Formulário para adicionar um comentário sobre um lugar específico.
    """
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Escreva seu comentário aqui...'
            }),
        }
