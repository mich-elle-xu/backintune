import requests
import time

esp32_ip = "http://172.26.175.168"
while True:
  requests.get(esp32_ip + "/red")   # Turn LED red
  time.sleep(1)
  requests.get(esp32_ip + "/green") # Turn LED green
  time.sleep(1)
  requests.get(esp32_ip + "/blue")  # Turn LED blue
  time.sleep(1)
  requests.get(esp32_ip + "/off")  # Turn LED off
  time.sleep(1)