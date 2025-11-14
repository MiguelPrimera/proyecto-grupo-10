from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import PublicacionForm
from .models import Publicaciones, UnionGrupo
from django.contrib.auth.decorators import login_required
from .models import Disponibilidad

def home(request):
    return render(request, 'myapp/home.html')

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

@login_required(login_url='mensaje')
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.creador = request.user
            publicacion.save()
            messages.success(request, 'Publicación creada correctamente.')
            return redirect('lista_publicaciones')
    else:
        form = PublicacionForm()
    return render(request, 'myapp/crear_publicacion.html', {'form': form})

@login_required(login_url='mensaje')
def lista_publicaciones(request):

    publicaciones = Publicaciones.objects.all().order_by('-fecha_creacion')
    usuario = request.user
    grupos_unidos = UnionGrupo.objects.filter(usuario=usuario).values_list('publicacion_id', flat=True)
    unido = UnionGrupo.objects.filter(usuario=usuario)

    return render(request, 'myapp/lista_publicaciones.html', {
        'publicaciones': publicaciones,
        'grupos_unidos': grupos_unidos,
        'unido': unido
    })


@login_required
def unirse_grupo(request, publicacion_id):
    publicacion = get_object_or_404(Publicaciones, pk=publicacion_id)

    # Solo si hay cupos disponibles
    if publicacion.cupos_disponibles > 0:
        UnionGrupo.objects.get_or_create(usuario=request.user, publicacion=publicacion)
        publicacion.cupos_disponibles -= 1
        publicacion.save()
        messages.success(request, f'Te has unido al grupo "{publicacion.titulo}".')
    else:
        messages.error(request, 'No quedan cupos disponibles.')

    return redirect('lista_publicaciones')


@login_required
def salir_grupo(request, publicacion_id):
    publicacion = get_object_or_404(Publicaciones, pk=publicacion_id)
    union = UnionGrupo.objects.filter(usuario=request.user, publicacion=publicacion).first()

    if union:
        union.delete()
        publicacion.cupos_disponibles += 1
        publicacion.save()
        messages.success(request, f'Has salido del grupo "{publicacion.titulo}".')

    return redirect('lista_publicaciones')

@login_required(login_url='mensaje')
def borrar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicaciones, pk=publicacion_id)

    if publicacion.creador != request.user:
        messages.error(request, 'No tienes permiso para borrar esta publicación.')
    else:
        publicacion.delete()
        messages.success(request, 'Publicación eliminada correctamente.')

    return redirect('lista_publicaciones')

def seleccion_piso(request):
    return render(request, 'myapp/seleccion_piso.html')

def mapa_piso_1(request):
    return render(request, 'myapp/mapa_piso_1.html')

def mapa_piso_2(request):
    return render(request, 'myapp/mapa_piso_2.html')

def mapa_piso_3(request):
    return render(request, 'myapp/mapa_piso_3.html')

def mapa_piso_4(request):
    return render(request, 'myapp/mapa_piso_4.html')

def coords(request):  #para facilitar encontrar las coordenadas en pixeles
    return render(request, 'myapp/coords.html')

def salas_piso_1(request):

    # Obtener nombre del edificio que se hizo clic en el mapa
    edificio_seleccionado = request.GET.get("edificio")

    # Todas las salas libres del piso 1
    info = Disponibilidad.objects.filter(
        sala__piso__numero=1,
        estado='Libre'
    ).select_related('sala', 'bloque')

    data = {}
    for d in info:
        edificio = 'Edificio ' + d.sala.nombre[0]

        if edificio not in data:
            data[edificio] = {
                "Lunes": {}, "Martes": {}, "Miércoles": {},
                "Jueves": {}, "Viernes": {}
            }

        dia = d.dia.nombre
        sala = d.sala.nombre

        if sala not in data[edificio][dia]:
            data[edificio][dia][sala] = []

        data[edificio][dia][sala].append(d.bloque.nombre)

    # SI se escogió un edificio, filtramos
    if edificio_seleccionado in data:
        data = {edificio_seleccionado: data[edificio_seleccionado]}

    return render(request, 'myapp/salas_piso_1.html', {
        'data': data,
        'edificio_seleccionado': edificio_seleccionado,
    })

def salas_piso_2(request):

    edificio_seleccionado = request.GET.get("edificio")

    info = Disponibilidad.objects.filter(
        sala__piso__numero=2,
        estado='Libre'
    ).select_related('sala', 'bloque')

    data = {}
    for d in info:
        edificio = 'Edificio ' + d.sala.nombre[0]

        if edificio not in data:
            data[edificio] = {
                "Lunes": {}, "Martes": {}, "Miércoles": {},
                "Jueves": {}, "Viernes": {}
            }

        dia = d.dia.nombre
        sala = d.sala.nombre

        if sala not in data[edificio][dia]:
            data[edificio][dia][sala] = []

        data[edificio][dia][sala].append(d.bloque.nombre)

    if edificio_seleccionado in data:
        data = {edificio_seleccionado: data[edificio_seleccionado]}

    return render(request, 'myapp/salas_piso_2.html', {
        'data': data,
        'edificio_seleccionado': edificio_seleccionado,
    })

def salas_piso_3(request):

    edificio_seleccionado = request.GET.get("edificio")

    info = Disponibilidad.objects.filter(
        sala__piso__numero=3,
        estado='Libre'
    ).select_related('sala', 'bloque')

    data = {}
    for d in info:
        edificio = 'Edificio ' + d.sala.nombre[0]

        if edificio not in data:
            data[edificio] = {
                "Lunes": {}, "Martes": {}, "Miércoles": {},
                "Jueves": {}, "Viernes": {}
            }

        dia = d.dia.nombre
        sala = d.sala.nombre

        if sala not in data[edificio][dia]:
            data[edificio][dia][sala] = []

        data[edificio][dia][sala].append(d.bloque.nombre)

    if edificio_seleccionado in data:
        data = {edificio_seleccionado: data[edificio_seleccionado]}

    return render(request, 'myapp/salas_piso_3.html', {
        'data': data,
        'edificio_seleccionado': edificio_seleccionado,
    })

def salas_piso_4(request):

    edificio_seleccionado = request.GET.get("edificio")

    info = Disponibilidad.objects.filter(
        sala__piso__numero=4,
        estado='Libre'
    ).select_related('sala', 'bloque')

    data = {}
    for d in info:
        edificio = 'Edificio ' + d.sala.nombre[0]

        if edificio not in data:
            data[edificio] = {
                "Lunes": {}, "Martes": {}, "Miércoles": {},
                "Jueves": {}, "Viernes": {}
            }

        dia = d.dia.nombre
        sala = d.sala.nombre

        if sala not in data[edificio][dia]:
            data[edificio][dia][sala] = []

        data[edificio][dia][sala].append(d.bloque.nombre)

    if edificio_seleccionado in data:
        data = {edificio_seleccionado: data[edificio_seleccionado]}

    return render(request, 'myapp/salas_piso_4.html', {
        'data': data,
        'edificio_seleccionado': edificio_seleccionado,
    })

def mensaje(request):
    return render(request, 'myapp/mensaje.html')