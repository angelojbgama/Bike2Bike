from django.contrib import admin
from .models import Lugar

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'latitude', 'longitude')
