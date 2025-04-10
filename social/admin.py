# admin.py
from django.contrib import admin
from .models import Post

# Cria um filtro customizado para o campo bike_trajectory
class BikeTrajectoryFilter(admin.SimpleListFilter):
    title = 'Trajeto de Bike'
    parameter_name = 'bike_trajectory'

    def lookups(self, request, model_admin):
        # Define as opções: 'preenchido' e 'vazio'
        return (
            ('filled', 'Preenchido'),
            ('empty', 'Vazio'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'filled':
            # Filtra os posts onde bike_trajectory não é nulo e não está vazio
            return queryset.exclude(bike_trajectory__isnull=True).exclude(bike_trajectory="")
        if value == 'empty':
            # Filtra os posts onde bike_trajectory é nulo ou vazio
            return queryset.filter(bike_trajectory__isnull=True) | queryset.filter(bike_trajectory="")
        return queryset

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Exibe os campos id, usuário, data de criação e se o trajeto está preenchido
    list_display = ('id', 'user', 'created_at', 'has_bike_trajectory')
    # Acrescenta o filtro customizado para bike_trajectory, além de outros filtros que desejar
    list_filter = (BikeTrajectoryFilter, 'user', 'created_at',)
    search_fields = ('id', 'user__username', 'title',)

    # Método customizado para verificar se bike_trajectory está preenchido (retorna True ou False)
    def has_bike_trajectory(self, obj):
        return bool(obj.bike_trajectory)
    has_bike_trajectory.boolean = True  # Exibe um ícone de check ou x
    has_bike_trajectory.short_description = 'Trajeto Preenchido?'
