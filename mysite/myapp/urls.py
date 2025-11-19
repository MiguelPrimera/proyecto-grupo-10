from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('grupos_publicados', views.grupos_publicados, name='grupos_publicados'),
    path('crear_publicacion/', views.crear_publicacion, name='crear_publicacion'),
    path('unirse_grupo/<int:publicacion_id>/', views.unirse_grupo, name='unirse_grupo'),
    path('salir_grupo/<int:publicacion_id>/', views.salir_grupo, name='salir_grupo'),
    path('borrar_publicacion/<int:publicacion_id>/', views.borrar_publicacion, name='borrar_publicacion'),
    path('expulsar_miembro/<int:union_id>/', views.expulsar_miembro, name='expulsar_miembro'),
    path('mapa_piso_1/', views.mapa_piso_1, name='mapa_piso_1'),
    path('mapa_piso_2/', views.mapa_piso_2, name='mapa_piso_2'),
    path('mapa_piso_3/', views.mapa_piso_3, name='mapa_piso_3'),
    path('mapa_piso_4/', views.mapa_piso_4, name='mapa_piso_4'),
    path('salas_piso_1/', views.salas_piso_1, name='salas_piso_1'),
    path('salas_piso_2/', views.salas_piso_2, name='salas_piso_2'),
    path('salas_piso_3/', views.salas_piso_3, name='salas_piso_3'),
    path('salas_piso_4/', views.salas_piso_4, name='salas_piso_4'),
    path('coords/',views.coords,name='coords'), #para facilitar encontrar las coordenadas en pixeles
    path('mensaje/', views.mensaje, name='mensaje')
]