from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import PublicacionForm
from .models import Publicacion
from .models import Disponibilidad

def home(request):
    return render(request, 'myapp/home.html')

def prueba(request):
    return render(request, 'myapp/prueba.html', {'lista':["uno", "dos", "tres"]})

def register(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, "Debes completar todos los campos.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('register')


        user = User.objects.create_user(
            username=username,
            password=password1
        )

        login(request, user)
        messages.success(request, "Usuario creado exitosamente.")
        return redirect('home')
    return render(request, 'myapp/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return render(request, 'myapp/login.html')

    return render(request, 'myapp/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')

def crear(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = PublicacionForm()
    return render(request, 'myapp/crear.html', {'form': form})

def lista(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'myapp/lista.html', {'publicaciones': publicaciones})

def mapa(request):
    return render(request, 'myapp/mapa.html')

def salas_piso_1(request):
    info=Disponibilidad.objects.filter(sala__piso__numero=1, estado='Libre').select_related('sala', 'bloque')
    lunes={}
    martes={}
    miercoles={}
    jueves={}
    viernes={}
    for d in info:
        if d.dia.nombre=="Lunes":
            sala_nombre=d.sala.nombre
            if sala_nombre not in lunes:
                lunes[sala_nombre]=[]
            lunes[sala_nombre].append(d.bloque.nombre)
        elif d.dia.nombre=="Martes":
            sala_nombre=d.sala.nombre
            if sala_nombre not in martes:
                martes[sala_nombre]=[]
            martes[sala_nombre].append(d.bloque.nombre)
        elif d.dia.nombre=="Miércoles":
            sala_nombre=d.sala.nombre
            if sala_nombre not in miercoles:
                miercoles[sala_nombre]=[]
            miercoles[sala_nombre].append(d.bloque.nombre)
        elif d.dia.nombre=="Jueves":
            sala_nombre=d.sala.nombre
            if sala_nombre not in jueves:
                jueves[sala_nombre]=[]
            jueves[sala_nombre].append(d.bloque.nombre)
        elif d.dia.nombre=="Viernes":
            sala_nombre=d.sala.nombre
            if sala_nombre not in viernes:
                viernes[sala_nombre]=[]
            viernes[sala_nombre].append(d.bloque.nombre)
        
    return render(request, 'myapp/salas_piso_1.html', {'lunes': lunes,'martes': martes,'miercoles': miercoles,'jueves': jueves,'viernes': viernes})

