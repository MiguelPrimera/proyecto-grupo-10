from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prueba/', views.prueba, name='prueba'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('crear/', views.crear, name='crear'),
    path('lista/', views.lista, name='lista'),
    path('mapa/', views.mapa, name='mapa'),
    path('salas_piso_1/', views.salas_piso_1, name='salas_piso_1'),
    path('salas_piso_2/', views.salas_piso_2, name='salas_piso_2'),
    path('salas_piso_3/', views.salas_piso_3, name='salas_piso_3'),
    path('salas_piso_4/', views.salas_piso_4, name='salas_piso_4')
]