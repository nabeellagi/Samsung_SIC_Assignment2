import urequests

FLASK_API_URL = "http://192.168.75.196:5000"  # Ensure this IP is correct
FLASK_MOTION1_ENDPOINT = f"{FLASK_API_URL}/motion/1/"
FLASK_MOTION2_ENDPOINT = f"{FLASK_API_URL}/motion/2/"
FLASK_SUMMOTION_ENDPOINT = f"{FLASK_API_URL}/summotion"

def send_to_flask(endpoint, data):
    try:
        headers = {"Content-Type": "application/json"}
        print("Sending data to Flask:", endpoint, data)
        response = urequests.post(endpoint, json=data, headers=headers)
        print("Response from Flask:", response.text)
    except Exception as e:
        print("Error sending data to Flask:", e)
    finally:
        try:
            response.close()
        except:
            pass  # Ensure response is closed safely

def check_server():
    try:
        response = urequests.get(FLASK_API_URL, timeout=3)
        if response.status_code == 200:
            print("Flask server is up!")
        response.close()
    except:
        print("Flask server is unreachable!")

check_server()
