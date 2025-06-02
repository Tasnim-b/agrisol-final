from django.contrib import admin
from .models import Agriculteur,Alerte,Plante,Culture,Mesure,Intervalle 

# Register your models here.
admin.site.register(Agriculteur)
admin.site.register(Alerte)
admin.site.register(Culture)
admin.site.register(Plante)
admin.site.register(Mesure)
admin.site.register(Intervalle)
#mdp 123456