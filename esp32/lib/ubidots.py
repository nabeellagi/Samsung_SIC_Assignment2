UBIDOTS_TOKEN = "BBUS-rbNI9xncF4ITokrgRowl1qafeEfxfy"
DEVICE_LABEL = "prototype_sic_futurepulse"
VARIABLE_LABELS = ["motion1", "motion2", "sum_motion"]

def send_to_ubidots(client, motion1, motion2, sum_motion=None):
    """Send motion sensor data to Ubidots via MQTT."""
    topic = f"/v1.6/devices/{DEVICE_LABEL}"
    
    if sum_motion is None:
        # Send only motion1 and motion2
        payload = f'{{"{VARIABLE_LABELS[0]}": {motion1}, "{VARIABLE_LABELS[1]}": {motion2}}}'
    else:
        # Send sum_motion
        payload = f'{{"{VARIABLE_LABELS[2]}": {sum_motion}}}'
    
    try:
        client.publish(topic, payload)
        print("Data sent to Ubidots:", payload)
    except Exception as e:
        print("Error sending data:", e)
