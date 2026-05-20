from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Animal, Profile, InteresseAdocao

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
    adotado = request.GET.get('adotado') == '1'
    
    if adotado:
        if request.user.is_authenticated:
            # Create a real interest record
            InteresseAdocao.objects.get_or_create(animal=animal, usuario=request.user)
        else:
            # Redirect to login with next path
            messages.info(request, "Por favor, faça login para manifestar interesse de adoção.")
            return redirect(f"/login/?next={request.path}%3Fadotado%3D1")
            
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

def view_cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')
        
        if not nome or not email or not telefone or not senha:
            messages.error(request, "Todos os campos são obrigatórios.")
            return render(request, 'cadastro.html')
            
        if User.objects.filter(username=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return render(request, 'cadastro.html')
            
        try:
            # create_user expects: username, email, password
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            # Create Profile
            Profile.objects.create(user=user, telefone=telefone)
            # Log the user in
            login(request, user)
            messages.success(request, f"Cadastro realizado com sucesso! Bem-vindo(a), {nome}!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro ao realizar cadastro: {str(e)}")
            return render(request, 'cadastro.html')
            
    return render(request, 'cadastro.html')

def view_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not email or not senha:
            messages.error(request, "E-mail e senha são obrigatórios.")
            return render(request, 'login.html', {'next': next_url})
            
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo(a) de volta, {user.first_name or user.username}!")
            if next_url and next_url != 'home':
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "E-mail ou senha incorretos.")
            return render(request, 'login.html', {'next': next_url})
            
    return render(request, 'login.html', {'next': next_url})

def view_logout(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home')

@login_required(login_url='login')
def view_perfil(request):
    # Ensure profile exists (in case user was created without one)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        
        if not nome or not email:
            messages.error(request, "Nome e E-mail são obrigatórios.")
        else:
            try:
                request.user.first_name = nome
                request.user.email = email
                request.user.username = email  # Keep username in sync with email
                request.user.save()
                
                profile.telefone = telefone
                profile.save()
                
                messages.success(request, "Seus dados foram atualizados com sucesso!")
                return redirect('perfil')
            except Exception as e:
                messages.error(request, f"Erro ao atualizar dados: {str(e)}")
                
    # Retrieve user's interests
    interesses = request.user.meus_interesses.all().select_related('animal')
    
    context = {
        'profile': profile,
        'interesses': interesses,
    }
    return render(request, 'perfil.html', context)


