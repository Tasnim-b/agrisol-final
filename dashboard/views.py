from functools import wraps
from django.core.cache import cache
import requests
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AgriculteurForm, PasswordChangeForm
from .models import Agriculteur, Culture, Mesure, Plante, Alerte


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = AgriculteurForm(request.POST)
        if form.is_valid():
            # Création manuelle de l'agriculteur
            agriculteur = form.save(commit=False)
            
            # ⚠️ Dans une vraie app, tu devrais hasher le mot de passe !
            # Exemple : agriculteur.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])
            agriculteur.save()

            messages.success(request, "Inscription réussie !")
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = AgriculteurForm()
    return render(request, 'register.html', {'form': form})


MAX_ATTEMPTS = 5
BLOCK_TIME = 15 * 60  # 15 minutes en secondes

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        cache_key_attempts = f'login_attempts_{email}'
        cache_key_blocked = f'login_blocked_{email}'

        # Vérifier si l'utilisateur est bloqué
        if cache.get(cache_key_blocked):
            messages.error(request, "Trop de tentatives échouées. Veuillez réessayer dans 15 minutes.")
            return render(request, 'login.html')

        try:
            agriculteur = Agriculteur.objects.get(email=email)
            
            if check_password(password, agriculteur.mot_de_passe):
                # Connexion réussie => supprimer compteur d'échecs
                cache.delete(cache_key_attempts)
                request.session['agriculteur_id'] = agriculteur.id
                request.session['agriculteur_email'] = agriculteur.email
                messages.success(request, "Connexion réussie !")
                return redirect('home')
            else:
                # Mauvais mot de passe => incrémenter compteur
                attempts = cache.get(cache_key_attempts, 0) + 1
                cache.set(cache_key_attempts, attempts, timeout=BLOCK_TIME)
                if attempts >= MAX_ATTEMPTS:
                    # Bloquer l'utilisateur
                    cache.set(cache_key_blocked, True, timeout=BLOCK_TIME)
                    cache.delete(cache_key_attempts)
                    messages.error(request, "Trop de tentatives échouées. Votre compte est bloqué pour 15 minutes.")
                else:
                    messages.error(request, f"Mot de passe incorrect. Il vous reste {MAX_ATTEMPTS - attempts} tentative(s).")
        except Agriculteur.DoesNotExist:
            messages.error(request, "Aucun compte avec cet email.")
    
    return render(request, 'login.html')

def logout_view(request):
    if 'agriculteur_id' in request.session:
        del request.session['agriculteur_id']
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('home')

def agriculteur_est_connecte(request):
    return 'agriculteur_id' in request.session
def login_required_custom(view_func):
 
    @wraps(view_func)  # Préserve les métadonnées de la fonction originale
    def wrapper(request, *args, **kwargs):
        if 'agriculteur_id' not in request.session:
            messages.error(request, "Veuillez vous connecter pour accéder à cette page.")
            return redirect('login')  # Remplace 'login' par le nom de ta URL de connexion
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def home(request):
    # Exemple de vue protégée
    agriculteur_id = request.session.get('agriculteur_id')
    agriculteur = Agriculteur.objects.get(id=agriculteur_id)
    return render(request, 'home.html', {'agriculteur': agriculteur})



@login_required_custom
def profil(request):
    agriculteur = Agriculteur.objects.get(id=request.session['agriculteur_id'])
    if request.method == 'POST':
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        if email:
            agriculteur.email = email
        else:
            # Si l'email est vide, conserve l'email existant
            messages.error(request, "L'email ne peut pas être vide.")
            return redirect('profil')
        
        agriculteur.telephone = telephone
        agriculteur.nom = nom
        agriculteur.prenom = prenom
        agriculteur.save()

        messages.success(request, 'Profil mis à jour avec succès.')
        return redirect('profil')  # Rediriger vers la page de profil après enregistrement

    return render(request, 'profil.html', {'agriculteur': agriculteur})
@login_required_custom
def change_password(request):
    # Vérification plus robuste du profil agriculteur
    try:
        agriculteur = request.user.agriculteur
    except (AttributeError, Agriculteur.DoesNotExist):
        messages.error(request, "Profil agriculteur non trouvé. Veuillez contacter l'administrateur.")
        return redirect('profil')
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mot de passe mis à jour avec succès!')
            
            agriculteur.password_last_updated = timezone.now()
            agriculteur.save()
            
            return redirect('profil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'dashboard/change_password.html', {
        'form': form,
        'agriculteur': agriculteur
    })

@login_required_custom
def temperature_dashboard(request):
    try:
        # Récupérez les données de température depuis votre modèle ou API
        # Exemple avec des données simulées :
        context = {
            'current_temp': 24.5,
            'temp_data': {
                'labels': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
                'values': [22, 24, 25, 23, 26, 28, 24]
            },
            'max_temp': 28,
            'min_temp': 18,
            'optimal_temp': 22,
            'alert_threshold': 30
        }
        return render(request, 'dashboard/temperature.html', context)
    
    except Exception as e:
        messages.error(request, f"Erreur de chargement des données: {str(e)}")
        return redirect('home')

@login_required_custom
def dashboard_view(request, culture_id=None):
    try:
        agriculteur_id = request.session['agriculteur_id']
        agriculteur = Agriculteur.objects.get(id=agriculteur_id)
        
        context = {
            'agriculteur': agriculteur,
            'nom': 'Aucune culture sélectionnée',
            # Valeurs par défaut
            'humidity': 0,
            'temperature': 0,
            'lumiere': 0,
            'N_eau': 0,
            'ph': 0,
            'co2': 0,
            'chart_labels': [],
            'humidity_data': [],
            'temperature_data': [],
            'niveau_d_eau_data': [],
            'ph_data': [],
            'co2_data': [],
            'lumiere_data': [],
            'intervalles': None  # Ajout des intervalles optimaux
        }

        if culture_id:
            culture = get_object_or_404(Culture, id=culture_id, agriculteur=agriculteur)
            context['nom'] = culture.plante.nom
            context['culture'] = culture  # Ajout de l'objet culture au contexte
            
            # Récupérer les intervalles optimaux de la plante
            plante = culture.plante
            context['intervalles'] = {
                'temperature': {'min': plante.temperature.min, 'max': plante.temperature.max},
                'humidite': {'min': plante.humidite.min, 'max': plante.humidite.max},
                'ph': {'min': plante.ph.min, 'max': plante.ph.max},
                'niveau_eau': {'min': plante.niveau_eau.min, 'max': plante.niveau_eau.max},
                'co2': {'min': plante.co2.min, 'max': plante.co2.max},
                'lumiere': {'min': plante.lumiere.min, 'max': plante.lumiere.max},
            }
            
            # Récupérer les mesures existantes
            mesures = Mesure.objects.filter(culture=culture).order_by('-timestamp')[:10]
            
            if mesures.exists():
                derniere_mesure = mesures.first()
                valeurs = derniere_mesure.valeurs
                
                # Mettre à jour les valeurs avec celles de la dernière mesure
                context.update({
                    'humidity': valeurs.get('humidite', 0),
                    'temperature': valeurs.get('temperature', 0),
                    'lumiere': valeurs.get('lumiere', 0),
                    'N_eau': valeurs.get('niveau_eau', 0),
                    'ph': valeurs.get('ph', 0),
                    'co2': valeurs.get('co2', 0),
                })
                
                # Préparer les données pour les graphiques
                mesures = list(mesures.reverse())  # Ordre chronologique
                context['chart_labels'] = [m.timestamp.strftime('%H:%M') for m in mesures]
                context['humidity_data'] = [m.valeurs.get('humidite', 0) for m in mesures]
                context['temperature_data'] = [m.valeurs.get('temperature', 0) for m in mesures]
                context['niveau_d_eau_data'] = [m.valeurs.get('niveau_eau', 0) for m in mesures]
                context['ph_data'] = [m.valeurs.get('ph', 0) for m in mesures]
                context['co2_data'] = [m.valeurs.get('co2', 0) for m in mesures]
                context['lumiere_data'] = [m.valeurs.get('lumiere', 0) for m in mesures]
        
        return render(request, 'dashboard.html', context)
        
    except KeyError:
        messages.error(request, "Session invalide, veuillez vous reconnecter")
        return redirect('login')
    except Agriculteur.DoesNotExist:
        messages.error(request, "Profil agriculteur introuvable")
        return redirect('login')
@login_required_custom
def mes_cultures(request):
    agriculteur_id = request.session.get('agriculteur_id')
    agriculteur = get_object_or_404(Agriculteur, id=agriculteur_id)

    if request.method == 'POST':
        plante_id = request.POST.get('plante_id')
        if not plante_id:
            messages.error(request, "Aucune plante sélectionnée")
            return redirect('mes_cultures')
            
        try:
            plante = Plante.objects.get(id=plante_id)
            
            # Créer une nouvelle culture avec un nom unique
            culture = Culture(
                nomCulture=f"Culture {plante.nom} - {timezone.now().strftime('%Y-%m-%d')}",
                plante=plante,
                agriculteur=agriculteur
            )
            culture.save()  # Sauvegarde effective dans la base de données
            
            messages.success(request, f"Culture de {plante.nom} ajoutée avec succès!")
            return redirect('mes_cultures')
            
        except Plante.DoesNotExist:
            messages.error(request, "Plante introuvable")
            return redirect('mes_cultures')

    # Récupérer les cultures existantes et les plantes disponibles
    cultures_existantes = Culture.objects.filter(agriculteur=agriculteur).order_by('-date_creation')
    plantes = Plante.objects.all()

    return render(request, 'mes_cultures.html', {
        'cultures': cultures_existantes,
        'plantes': plantes
    })
@login_required_custom
def delete_culture(request, culture_id):
    agriculteur_id = request.session.get('agriculteur_id')
    agriculteur = Agriculteur.objects.get(id=agriculteur_id)
    
    culture = get_object_or_404(Culture, id=culture_id, agriculteur=agriculteur)
    
    if request.method == 'POST':
        culture.delete()
        return redirect('mes_cultures')
    
    return redirect('mes_cultures')
# @login_required_custom
# def alert(request):
#     # Exemple de vue protégée
#     agriculteur_id = request.session.get('agriculteur_id')
#     agriculteur = Agriculteur.objects.get(id=agriculteur_id)
#     return render(request, 'alert.html', {'agriculteur': agriculteur})




def meteo_view(request):
    api_key = "c4d21364a755246057ed4504b0e509e1"
    
    villes_disponibles = [
        "Ariana", "Béja", "Ben Arous", "Bizerte", "Gabès",
        "Gafsa", "Jendouba", "Kairouan", "Kasserine", "Kebili",
        "Kef", "Mahdia", "Manouba", "Médenine", "Monastir",
        "Nabeul", "Sfax", "Sidi Bouzid", "Siliana", "Sousse",
        "Tataouine", "Tozeur", "Tunis", "Zaghouan"
    ]
    
    # Récupérer la ville sélectionnée ou utiliser Tunis par défaut
    ville = request.GET.get('ville', "Tunis")
    
    # Récupérer les données météo actuelles
    url_actuel = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
    
    try:
        response_actuel = requests.get(url_actuel)
        response_actuel.raise_for_status()  # Vérifier les erreurs HTTP
        data_actuel = response_actuel.json()
        
        # Formater les données actuelles
        meteo_actuel = {
            "ville": ville,
            "temperature": data_actuel["main"]["temp"],
            "ressenti": data_actuel["main"]["feels_like"],
            "description": data_actuel["weather"][0]["description"].capitalize(),
            "humidite": data_actuel["main"]["humidity"],
            "vent": data_actuel["wind"]["speed"],
            "pression": data_actuel["main"]["pressure"],
            "icone": data_actuel["weather"][0]["icon"],
            "lever_soleil": datetime.fromtimestamp(data_actuel["sys"]["sunrise"]).strftime('%H:%M'),
            "coucher_soleil": datetime.fromtimestamp(data_actuel["sys"]["sunset"]).strftime('%H:%M')
        }
    except Exception as e:
        meteo_actuel = {
            "error": f"Erreur lors de la récupération des données actuelles: {str(e)}"
        }
    
    # Récupérer les prévisions sur 5 jours
    url_previsions = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&appid={api_key}&units=metric&lang=fr"
    
    try:
        response_previsions = requests.get(url_previsions)
        response_previsions.raise_for_status()
        data_previsions = response_previsions.json()
        
        # Organiser les prévisions par jour
        previsions_par_jour = {}
        for prev in data_previsions['list']:
            date = datetime.fromtimestamp(prev['dt']).strftime('%Y-%m-%d')
            if date not in previsions_par_jour:
                previsions_par_jour[date] = []
            previsions_par_jour[date].append(prev)
        
        # Sélectionner la prévision la plus représentative pour chaque jour (midi)
        previsions = []
        for date, prevs in previsions_par_jour.items():
            # Trouver la prévision la plus proche de midi
            prev_midi = min(prevs, key=lambda p: abs(12 - datetime.fromtimestamp(p['dt']).hour))
            
            previsions.append({
                "date": date,
                "jour": datetime.fromtimestamp(prev_midi['dt']).strftime('%A'),
                "temperature": prev_midi['main']['temp'],
                "icone": prev_midi['weather'][0]['icon'],
                "description": prev_midi['weather'][0]['description'].capitalize()
            })
        
        # Ne garder que les 5 prochains jours
        previsions = previsions[1:6]
        
    except Exception as e:
        previsions = []
        print(f"Erreur prévisions: {str(e)}")

    contexte = {
        "meteo_actuel": meteo_actuel,
        "previsions": previsions,
        "villes": villes_disponibles
    }

    return render(request, 'meteo.html', contexte)


def alert(request):
    agriculteur_id = request.session.get('agriculteur_id')
    agriculteur = Agriculteur.objects.get(id=agriculteur_id)
    # Récupérer les alertes de l'agriculteur
    alertes = Alerte.objects.filter(agriculteur=request.user).order_by('-created_at')
    return render(request, 'alert.html', {'agriculteur': agriculteur, 'alertes': alertes})