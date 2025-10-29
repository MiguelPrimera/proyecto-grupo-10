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
    path('mapa/', views.mapa, name='mapa')
]