from django.contrib import admin
from .models import Lugar, Comentario

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'latitude', 'longitude')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('lugar', 'texto', 'data_criacao')
    search_fields = ('lugar__nome', 'texto')
    list_filter = ('data_criacao',)
