from django.contrib import admin
from .models import Animal, InteresseAdocao

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'idade', 'idade_categoria', 'tamanho', 'sexo', 'vacinado', 'castrado')
    list_filter = ('especie', 'idade_categoria', 'tamanho', 'sexo', 'vacinado', 'castrado')
    search_fields = ('nome', 'caracteristicas', 'descricao')
    list_per_page = 20
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'especie', 'foto', 'idade', 'idade_categoria', 'sexo', 'tamanho')
        }),
        ('Detalhes', {
            'fields': ('caracteristicas', 'descricao')
        }),
        ('Saúde', {
            'fields': ('vacinado', 'castrado')
        }),
    )

@admin.register(InteresseAdocao)
class InteresseAdocaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'animal', 'data_solicitacao')
    list_filter = ('animal', 'data_solicitacao')
    search_fields = ('usuario__username', 'animal__nome')
