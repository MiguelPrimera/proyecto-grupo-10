from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Dia, Bloque, Piso, Sala, Disponibilidad, Publicaciones, UnionGrupo

admin.site.register(Dia)
admin.site.register(Bloque)
admin.site.register(Piso)
admin.site.register(Sala)
admin.site.register(Disponibilidad)
admin.site.register(Publicaciones)
admin.site.register(UnionGrupo)