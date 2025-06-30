import network, urequests, machine, time

# ==== CONFIG ====
WIFI_SSID = 'Netcom_Wifi'
WIFI_PASS = '123456789'
FLASK_URL = 'http://10.10.10.3:5000/api/tasks'  # ← update to your PC’s LAN IP
BUTTON_PIN = 0  # change if needed
# ================

# Connect to Wi-Fi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(WIFI_SSID, WIFI_PASS)
while not sta.isconnected():
    time.sleep(1)
print('WiFi ok:', sta.ifconfig())

# Setup button
btn = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

def send_task(pin):
    try:
        res = urequests.post(FLASK_URL, json={"task": "Task done"})
        print('Sent:', res.text)
        res.close()
    except Exception as e:
        print('Error:', e)

# Debounce and IRQ
last = 0
def irq_handler(pin):
    global last
    now = time.ticks_ms()
    if time.ticks_diff(now, last) > 500:
        send_task(pin)
        last = now

btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=irq_handler)

# Keep alive
while True:
    time.sleep(10)
