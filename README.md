
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
### 🧩 Importer le flux dans Node-RED

Un fichier `flux.json` est fourni pour simplifier la mise en place du projet dans Node-RED.

### Étapes à suivre :

    1. Lancer Node-RED dans votre navigateur (par défaut : [http://localhost:1880](http://localhost:1880)).
    2. Cliquer sur le menu en haut à droite (☰).
    3. Aller dans **Import** > **Clipboard**.
    4. Copier tout le contenu du fichier `flows.json`.
    5. Coller ce contenu dans la fenêtre d'importation de Node-RED.
    6. Cliquer sur **Import**, puis sur **Deploy** pour démarrer le flux.
### 📄 Fichier `flows.json` à importer dans Node-RED
```bash
[
    {
        "id": "e25a4f4af894a469",
        "type": "tab",
        "label": "Flux 2",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "d2661a474e25346d",
        "type": "inject",
        "z": "e25a4f4af894a469",
        "name": "",
        "props": [
            {
                "p": "payload"
            },
            {
                "p": "topic",
                "vt": "str"
            }
        ],
        "repeat": "5",
        "crontab": "",
        "once": false,
        "onceDelay": "0.5",
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 270,
        "y": 260,
        "wires": [
            [
                "8d69445a8ee9250a"
            ]
        ]
    },
    {
        "id": "8d69445a8ee9250a",
        "type": "function",
        "z": "e25a4f4af894a469",
        "name": "function 3",
        "func": "let data = {\n    temperature: (20 + Math.random() * 10).toFixed(2),\n    humidity: (40 + Math.random() * 20).toFixed(2),\n    water_level: (Math.random() * 100).toFixed(1),\n    ph: (5 + Math.random() * 3).toFixed(2),\n    light: (Math.random() * 1000).toFixed(0),\n    co2: (300 + Math.random() * 400).toFixed(0)\n};\nmsg.payload = JSON.stringify(data);\nreturn msg;\n",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 720,
        "y": 240,
        "wires": [
            [
                "30bede21244df0fe",
                "456da6abfb11f09e"
            ]
        ]
    },
    {
        "id": "30bede21244df0fe",
        "type": "mqtt out",
        "z": "e25a4f4af894a469",
        "name": "",
        "topic": "agrisol/data",
        "qos": "0",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "f8d2f7cb347e622b",
        "x": 1130,
        "y": 280,
        "wires": []
    },
    {
        "id": "456da6abfb11f09e",
        "type": "debug",
        "z": "e25a4f4af894a469",
        "name": "debug 1",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "false",
        "statusVal": "",
        "statusType": "auto",
        "x": 1040,
        "y": 380,
        "wires": []
    },
    {
        "id": "f8d2f7cb347e622b",
        "type": "mqtt-broker",
        "name": "",
        "broker": "localhost",
        "port": 1883,
        "clientid": "",
        "autoConnect": true,
        "usetls": false,
        "protocolVersion": "5",
        "keepalive": 60,
        "cleansession": true,
        "autoUnsubscribe": true,
        "birthTopic": "",
        "birthQos": "0",
        "birthRetain": "false",
        "birthPayload": "",
        "birthMsg": {},
        "closeTopic": "",
        "closeQos": "0",
        "closeRetain": "false",
        "closePayload": "",
        "closeMsg": {},
        "willTopic": "",
        "willQos": "0",
        "willRetain": "false",
        "willPayload": "",
        "willMsg": {},
        "userProps": "",
        "sessionExpiry": ""
    }
]
```

### Lancez le serveur dans le terminal du projet 
```bash
daphne agrisol.asgi:application
```
## 🔐 Sécurité
- Authentification manuelle avec check_password
- Protection contre brute-force avec blocage temporaire
- Mots de passe hashés avec Django
