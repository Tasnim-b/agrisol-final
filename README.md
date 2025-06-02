
# 🌾 Agrisol — Système de Surveillance Agricole Intelligent

**Agrisol** est une plateforme Django permettant la communication en temps réel entre des dispositifs IoT (capteurs de température, humidité, etc.) et une interface web. Elle intègre MQTT pour recevoir les données des capteurs et utilise une base de données relationnelle pour le stockage .

---
## ⚙️ Fonctionnalités principales

- Enregistrement sécurisé des utilisateurs (agriculteurs).
- Authentification avec compteur d'échecs et blocage temporaire.
- Réception en temps réel des données IoT (température, humidité, etc.) envoyées par Node-RED via MQTT.
- Stockage des données de télémétrie (température, humidité, etc.).
- Affichage des prévisions météorologiques locales (via une API météo).

## 🚀 Installation

```bash
# Clonez le projet
git clone https://github.com/Tasnim-b/agrisol-final.git
cd agrisol
```
### Créez un environnement virtuel avec pipenv
```bash
pipenv install
```
### Activez l'environnement
```bash
pipenv shell
```
###  installer les dépendances
```bash
pip install -r requirements.txt
```
### Lancez les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### Installer Node-RED
```bash
npm install -g --unsafe-perm node-red
```

### dans le cmd lancez node-red
```bash
node-red
```
### Lancez le serveur dans le terminal du projet 
```bash
daphne agrisol.asgi:application
```
## 🔐 Sécurité
- Authentification manuelle avec check_password
- Protection contre brute-force avec blocage temporaire
- Mots de passe hashés avec Django
