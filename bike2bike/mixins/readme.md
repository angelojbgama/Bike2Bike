# Documentação do DaisyUIStyledFormMixin

O `DaisyUIStyledFormMixin` é um mixin para formulários Django que permite configurar dinamicamente atributos HTML e classes CSS dos campos com base em um dicionário de estilos definido na classe Meta do formulário. Esse mixin é ideal para integrar com frameworks CSS como Tailwind e DaisyUI, facilitando a criação de formulários estilizados e consistentes.

## Recursos Principais

* **Configuração via `field_styles`** : Define classes CSS, placeholders, tipos de input (como `datetime-local`), ícones e outros atributos para cada campo do formulário.
* **Validação Visual** : Adiciona classes de erro (ex.: `input-error`) quando um campo possui erros de validação.
* **Renderização Personalizada** : Gera o HTML para cada campo, incluindo ícones, mensagens de ajuda (hints) e mensagens de erro, com possibilidade de ocultá-las por padrão (usando a classe `hidden`).
* **Flexibilidade** : Permite definir atributos extras como `type`, `pattern`, `title`, etc., direto no dicionário de estilos.

---

## Estrutura do Código

### Atributos Padrão

* **default_input_class** : Classe padrão para inputs (ex.: `"input-bordered"`).
* **default_wrapper_class** : Classe padrão para o wrapper do campo (ex.: `"input validator items-center"`).
* **default_form_group_class** : Classe para o agrupamento do campo (ex.: `"form-control gap-1"`).

### Métodos

#### `get_field_styles(self)`

* **Descrição** : Recupera o dicionário de estilos definido em `Meta.field_styles` no formulário.
* **Retorno** : Um dicionário com as configurações de estilo para cada campo.

#### `__init__(self, *args, **kwargs)`

* **Descrição** : Construtor que itera sobre todos os campos do formulário, aplicando os estilos configurados.
* **Funcionalidades** :
* Verifica se o campo possui erro e adiciona a classe `input-error`.
* Adiciona a classe `grow` caso o campo possua ícones.
* Ajusta widgets especiais (Textarea, Select, FileInput).
* Configura atributos extras (ex.: `placeholder`, `type`, `pattern`, etc.) conforme definido em `field_styles`.

#### `render_field(self, name)`

* **Descrição** : Renderiza o HTML para um campo específico, incluindo ícones, hints, mensagens de erro e outros elementos.
* **Funcionalidades** :
* Recupera o `BoundField` do campo.
* Gera HTML para ícones à esquerda ou direita, mensagens de ajuda (hints) e erros.
* Se o campo for do tipo checkbox, aplica um layout especial.
* Por padrão, as mensagens de hint e de erro são renderizadas com a classe `hidden`, ficando ocultas até serem exibidas (por exemplo, via JavaScript ou quando os erros existirem).

#### `as_div(self)`

* **Descrição** : Renderiza todos os campos do formulário chamando o método `render_field` para cada um e concatenando o resultado.
* **Retorno** : Uma string contendo o HTML completo do formulário, com cada campo encapsulado em suas respectivas `<div>`s.

---

## Exemplo de Uso no Formulário

No exemplo a seguir, usamos o mixin em um formulário customizado. Observe como os estilos de cada campo são definidos em `Meta.field_styles`:

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bike2bike.mixins.DaisyUIFormMixin import DaisyUIStyledFormMixin

class CustomUserCreationForm(DaisyUIStyledFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Informe um e-mail válido.'
    )
    # Exemplo de campo adicional com tipo customizado
    data_hora = forms.DateTimeField(
        required=False,
        help_text='Selecione data e hora.'
    )

    class Meta:
        model = User
        fields = ("username", "email", "data_hora", "password1", "password2")
        field_styles = {
            "username": {
                "classes": "input-primary input-md",
                "icon": '<i class="fa fa-user h-[1em] opacity-50"></i>',
                "placeholder": "Usuário",
                "wrapper_class": "w-full",
                "row_class": "mb-4",
            },
            "email": {
                "classes": "input-info",
                "placeholder": "mail@site.com",
                "icon": '<i class="fa fa-envelope h-[1em] opacity-50"></i>',
                "row_class": "mb-4",
            },
            "data_hora": {
                "classes": "input-primary",
                "placeholder": "Selecione data e hora",
                "type": "datetime-local",  # Define o tipo do input
                "row_class": "mb-4",
            },
            "password1": {
                "classes": "input-success",
                "icon": '<i class="fa fa-key"></i>',
                "placeholder": "Senha forte",
                "hint": "Use pelo menos uma letra maiúscula, minúscula e um número",
                "type": "password",
                "pattern": "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "title": "Senha segura com maiúscula, minúscula e número",
                "row_class": "mb-4",
            },
            "password2": {
                "classes": "input-success",
                "icon": '<i class="fa fa-key"></i>',
                "placeholder": "Confirme a senha",
                "hint": "Use pelo menos uma letra maiúscula, minúscula e um número",
                "type": "password",
                "pattern": "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "title": "Senha segura com maiúscula, minúscula e número",
                "row_class": "mb-4",
            },
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
```

### Explicações do Exemplo

* **Campo `data_hora`** : É definido com o atributo `"type": "datetime-local"`, fazendo com que o input seja renderizado como `<input type="datetime-local" ...>`.
* **Espaçamento** : Cada campo possui o atributo `"row_class": "mb-4"`, adicionando uma margem inferior para separar os campos visualmente.
* **Ícones e Hints** : O campo `username` utiliza um ícone à esquerda e o campo `password1` e `password2` possuem dicas (hints) que, por padrão, ficam ocultas (classe `hidden`).

---

## Exemplo de Uso no Template

No template, você pode renderizar o formulário estilizado usando o método `as_div`:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Cadastro - Bike2Bike{% endblock %}

{% block content %}
<div class="flex flex-col items-center justify-center min-h-screen">
    <div class="card w-96 bg-base-200 shadow-xl">
        <div class="card-body">
            <h2 class="card-title justify-center">Cadastre-se</h2>
            <form method="post">
                {% csrf_token %}
                <!-- Renderiza todos os campos do formulário estilizado -->
                {{ form.as_div|safe }}
                <div class="form-control mt-6">
                    <button type="submit" class="btn btn-primary">Cadastrar</button>
                </div>
            </form>

            <div class="mt-4 text-center">
                <span>Já tem conta? </span>
                <a href="{% url 'login' %}" class="link link-info">Entre</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Notas Adicionais

* **Ocultação de Mensagens** : As mensagens de hint e erro são renderizadas com a classe `hidden`, ou seja, ficam ocultas até que um script ou a própria lógica do Django (após submissão inválida) as torne visíveis.
* **Personalização via JavaScript** : Caso queira exibir as mensagens dinamicamente (por exemplo, ao perder o foco do campo), basta escrever um script que remova a classe `hidden` quando necessário.

---

## Resumo

O `DaisyUIStyledFormMixin` facilita a personalização de formulários Django, permitindo que você defina estilos e atributos HTML de forma centralizada através do dicionário `field_styles`. Isso proporciona uma grande flexibilidade para integrar os formulários com frameworks de CSS modernos, mantendo o código limpo e consistente.

Este documento apresenta os métodos principais do mixin, explica como usá-lo no seu formulário e dá exemplos práticos tanto no backend (Python/Django) quanto na renderização via template. Adapte os exemplos conforme as necessidades do seu projeto.
