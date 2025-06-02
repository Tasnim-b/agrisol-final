# dashboard/alert_manager.py
from .models import Plante, Alerte, Agriculteur
from django.core.exceptions import ObjectDoesNotExist

def check_thresholds(data, user_id, plante_id=None):

    try:
        agriculteur = Agriculteur.objects.get(id=user_id)
        plante = Plante.objects.get(id=plante_id) if plante_id else None
        
        # Récupérer les seuils de la plante si disponible
        if plante:
            seuils = {
                'temperature': (plante.temperature.min, plante.temperature.max),
                'humidity': (plante.humidite.min, plante.humidite.max),
                'ph': (plante.ph.min, plante.ph.max),
                'water_level': (plante.niveau_eau.min, plante.niveau_eau.max),
                'light': (plante.lumiere.min, plante.lumiere.max),
                'co2': (plante.co2.min, plante.co2.max),
            }
        else:
            # Seuils par défaut si aucune plante spécifiée
            seuils = {
                'temperature': (18, 30),
                'humidity': (40, 80),
                'ph': (5.5, 7.5),
                'water_level': (20, 100),
                'light': (100, 30000),
                'co2': (300, 1000),
            }
        
        alertes_crees = []
        
        # Vérifier chaque paramètre
        for param, (min_val, max_val) in seuils.items():
            value = data.get(param)
            if value is None:
                continue
                
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
                
            message = ""
            niveau = "modéré"
            
            if value < min_val:
                niveau = "critique" if param in ['water_level', 'light'] else "modéré"
                message = f"{param.capitalize()} trop bas: {value} (min: {min_val})"
            elif value > max_val:
                niveau = "critique" if param in ['temperature', 'co2'] else "modéré"
                message = f"{param.capitalize()} trop haut: {value} (max: {max_val})"
            else:
                continue
                
            # Créer l'alerte
            alerte = Alerte.objects.create(
                agriculteur=agriculteur,
                type_alerte=param,
                valeur=value,
                seuil_min=min_val,
                seuil_max=max_val,
                niveau=niveau,
                message=message,
                plante_concernee=plante
            )
            alertes_crees.append(alerte)
            
        return alertes_crees
        
    except ObjectDoesNotExist as e:
        print(f"Objet non trouvé: {e}")
        return []
    except Exception as e:
        print(f"Erreur dans check_thresholds: {e}")
        return []