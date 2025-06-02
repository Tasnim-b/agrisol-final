from django.db import models
import datetime

# Intervalle des paramètres
class Intervalle(models.Model):
    min = models.FloatField()
    max = models.FloatField()

    def __str__(self):
        return f"Min: {self.min}, Max: {self.max}"

# Plante
class Plante(models.Model):
    nom = models.CharField(max_length=255)
    temperature = models.OneToOneField(Intervalle, related_name='temperature_plante', on_delete=models.CASCADE)
    humidite = models.OneToOneField(Intervalle, related_name='humidite_plante', on_delete=models.CASCADE)
    ph = models.OneToOneField(Intervalle, related_name='ph_plante', on_delete=models.CASCADE)
    niveau_eau = models.OneToOneField(Intervalle, related_name='niveau_eau_plante', on_delete=models.CASCADE)
    co2 = models.OneToOneField(Intervalle, related_name='co2_plante', on_delete=models.CASCADE)
    lumiere = models.OneToOneField(Intervalle, related_name='lumiere_plante', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

# Agriculteur
class Agriculteur(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='img/', blank=True, null=True)
    #class Meta: 
    #    table='agriculteur'

    def __str__(self):
        return f"{self.prenom} {self.nom}"



# Culture
class Culture(models.Model):
    nomCulture = models.CharField(max_length=255)
    plante = models.ForeignKey(Plante, on_delete=models.CASCADE)
    agriculteur = models.ForeignKey(Agriculteur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    mesures_en_temps_reel = models.JSONField(default=dict)  

    def __str__(self):
        return self.nomCulture

# Mesure
class Mesure(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    valeurs = models.JSONField() 

 
    def __str__(self):
        return f"Mesure pour {self.culture.nomCulture} à {self.timestamp}"

# Alerte
class Alerte(models.Model):
    NIVEAU_CHOICES = [
        ('faible', 'Faible'),
        ('modéré', 'Modéré'),
        ('critique', 'Critique'),
    ]
    TYPES_ALERTES = [
        ('humidity', 'Humidité'),
        ('ph', 'pH'),
        ('co2', 'CO2'),
        ('light', 'Lumière'),
        ('temperature', 'Température'),
        ('waterLevel', 'Niveau d\'eau'),
    ]

    agriculteur = models.ForeignKey('Agriculteur', on_delete=models.CASCADE, related_name='alertes', null=True, blank=True)
    type_alerte = models.CharField(max_length=20, choices=TYPES_ALERTES, default='humidity')  # valeur par défaut ajoutée
    valeur = models.FloatField()
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return f"Alerte {self.type_alerte} pour {self.agriculteur.email} à {self.created_at}"

