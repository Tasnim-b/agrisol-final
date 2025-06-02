import os
import sys
import django

# Ajouter le chemin du projet au chemin Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrisol.settings')
django.setup()

from dashboard.alert_manager import check_thresholds

# Données de test
test_data = {
    'temperature': 40,
    'humidity': 30,
    'water_level': 10,
    'ph': 8,
    'light': 50,
    'co2': 1200,
    'user_id': 1,
    'plante_id': 1
}

# Appeler la fonction
alertes = check_thresholds(test_data, test_data['user_id'], test_data['plante_id'])

print(f"Créées {len(alertes)} alertes:")
for alerte in alertes:
    print(f"- {alerte.message}")