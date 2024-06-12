from machine import Pin, Timer
import utime
import network
import time

# Configuration des broches
trigger = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)
led_green = Pin(17, Pin.OUT)
led_blue = Pin(20, Pin.OUT)
led_white = Pin(16, Pin.OUT)
led_red = Pin(18, Pin.OUT)

distance = 0

# Configuration Wi-Fi
ssid = 'A.B'
password = 'Aliabbas77777'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Fonction pour obtenir la distance
def get_distance(timer):
    global distance
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()

    start = utime.ticks_us()
    while echo.value() == 0:
        start = utime.ticks_us()
        
    stop = utime.ticks_us()
    while echo.value() == 1:
        stop = utime.ticks_us()
    
    print(f"Start: {start}, Stop: {stop}")
    
    duration = utime.ticks_diff(stop, start)
    distance = (duration * 0.0343) / 2
    print("Distance:", distance, "cm")


# Initialisation du timer
timer = Timer()
timer.init(freq=1, mode=Timer.PERIODIC, callback=get_distance)

# Attente de connexion Wi-Fi
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP = ' + status[0])

# Boucle principale
while True:
    if distance > 0 and distance < 100:
        led_red.value(1)
        led_white.value(0)
        led_blue.value(0)
        led_green.value(0)
    elif distance > 100 and distance < 104:
        led_red.value(0)
        led_white.value(1)
        led_blue.value(0)
        led_green.value(0)
    elif distance > 104 and distance < 107:
        led_red.value(0)
        led_white.value(0)
        led_blue.value(1)
        led_green.value(0)
    elif distance > 107 and distance < 150:
        led_red.value(0)
        led_white.value(0)
        led_blue.value(0)
        led_green.value(1)
    else:
        led_red.value(0)
        led_white.value(0)
        led_blue.value(0)
        led_green.value(0)
    utime.sleep(0.1)
