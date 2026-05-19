from django.shortcuts import render, get_object_or_404
from .models import Animal

def home(request):
    animais = Animal.objects.all()
    
    # Capturar parâmetros da URL para filtrar os animais
    especie = request.GET.get('especie')
    idade_categoria = request.GET.get('idade_categoria')
    tamanho = request.GET.get('tamanho')
    
    if especie and especie != 'Todos':
        animais = animais.filter(especie__iexact=especie)
        
    if idade_categoria and idade_categoria != 'Todos':
        animais = animais.filter(idade_categoria__iexact=idade_categoria)
        
    if tamanho and tamanho != 'Todos':
        animais = animais.filter(tamanho__iexact=tamanho)
        
    context = {
        'animais': animais,
        'selected_especie': especie or 'Todos',
        'selected_idade': idade_categoria or 'Todos',
        'selected_tamanho': tamanho or 'Todos',
    }
    return render(request, 'home.html', context)

def detalhe(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    # Suporta a simulação de adoção via parâmetro de URL
    adotado = request.GET.get('adotado') == '1'
    context = {
        'animal': animal,
        'adotado': adotado,
    }
    return render(request, 'detalhe.html', context)

def como_adotar(request):
    return render(request, 'como_adotar.html')

def sobre_nos(request):
    return render(request, 'sobre_nos.html')

def ongs(request):
    return render(request, 'ongs.html')


