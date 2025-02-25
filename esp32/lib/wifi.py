import network
from time import sleep

WIFI_SSID = "Halo"
WIFI_PASSWORD = "nabeel3588"

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            sleep(1)
    print("Connected to WiFi:", sta_if.ifconfig())
