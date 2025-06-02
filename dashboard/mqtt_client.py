import json
import threading
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from dashboard.alert_manager import check_thresholds

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"Received MQTT message: {data}")
     # Extraire les IDs
    user_id = data.get('user_id')
    plante_id = data.get('plante_id')
        
        # Vérifier les seuils et créer des alertes
    if user_id:
            check_thresholds(data, user_id, plante_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "sensor_data_group",  
        {
        "type": "send_sensor_data",  
        "message": data
        }
)

def mqtt_thread():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.subscribe("agrisol/data")
    client.on_message = on_message
    client.loop_forever()

def start():
    thread = threading.Thread(target=mqtt_thread)
    thread.daemon = True
    thread.start()