import network
from machine import Pin
from umqtt.simple import MQTTClient
from time import sleep

from lib.wifi import connect_wifi
from lib.ubidots import send_to_ubidots, UBIDOTS_TOKEN, DEVICE_LABEL
from lib.send_api import send_to_flask, FLASK_MOTION1_ENDPOINT, FLASK_MOTION2_ENDPOINT, FLASK_SUMMOTION_ENDPOINT

# GPIO Pin Configuration
PIR1 = Pin(13, Pin.IN)  # First PIR sensor
PIR2 = Pin(15, Pin.IN)  # Second PIR sensor
LED = Pin(2, Pin.OUT)   # LED indicator

MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_USER = UBIDOTS_TOKEN
MQTT_PASSWORD = ""

sum_motion = 0  # Sum of motion1 and motion2 over 60 seconds

def mqtt_callback(topic, msg):
    print("Message received:", topic, msg)

def setup_mqtt():
    """Initialize MQTT connection."""
    client = MQTTClient(
        client_id=DEVICE_LABEL,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD
    )
    client.set_callback(mqtt_callback)
    client.connect()
    print("Connected to Ubidots MQTT broker")
    return client

# Main execution
connect_wifi()
client = setup_mqtt()

# Timers
motion_publish_interval = 2
sum_motion_publish_interval = 60
send_api_interval = 40

motion_timer = 0
sum_motion_timer = 0
send_api_timer = 0

while True:
    motion1 = PIR1.value()
    motion2 = PIR2.value()

    sum_motion += (motion1 + motion2)

    # LED feedback based on either PIR sensor detecting motion
    if motion1 or motion2:
        print("Motion detected! Turning on LED.")
        LED.value(1)
    else:
        print("No motion detected. Turning off LED.")
        LED.value(0)

    # Publish motion1 and motion2 every 5 seconds
    if motion_timer >= motion_publish_interval:
        send_to_ubidots(client, motion1, motion2)
        
        motion_timer = 0  # Reset motion timer

    # Publish sum_motion every 60 seconds
    if sum_motion_timer >= sum_motion_publish_interval:
        send_to_ubidots(client, motion1, motion2, sum_motion)
        
        sum_motion = 0  # Reset sum_motion after publishing
        sum_motion_timer = 0  # Reset sum_motion timer
    
    if send_api_timer >= send_api_interval:
        send_to_flask(FLASK_MOTION1_ENDPOINT, {"motion": motion1})
        send_to_flask(FLASK_MOTION2_ENDPOINT, {"motion": motion2})
        send_to_flask(FLASK_SUMMOTION_ENDPOINT, {"sum_motion": sum_motion})
        
        send_api_timer = 0
    

    motion_timer += 1
    sum_motion_timer += 1
    send_api_timer += 1
    sleep(1)  # Wait before next reading

