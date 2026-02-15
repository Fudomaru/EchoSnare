import network
import time
import json
import os
from machine import Pin, ADC
import oled_driver

alive_led = Pin(35, Pin.OUT)
alive_led.on()

oled, vext = oled_driver.init_oled()

# Read battery voltage
def get_battery_voltage():
    """Read battery voltage from ADC"""
    adc_ctrl = Pin(37, Pin.OUT)
    adc_ctrl.value(1)  # HIGH for V3.2 boards
    time.sleep(0.01)
    
    battery_adc = ADC(Pin(1))
    battery_adc.atten(ADC.ATTN_11DB)
    
    voltage_uv = battery_adc.read_uv()
    adc_voltage = voltage_uv / 1000000
    battery_voltage = adc_voltage * 4.9  # Voltage divider scaling
    
    adc_ctrl.value(0)  # Disable to save power
    return battery_voltage

def get_battery_percent(voltage):
    """Convert voltage to approximate percentage"""
    if voltage >= 4.2:
        return 100
    elif voltage <= 3.0:
        return 0
    else:
        return int((voltage - 3.0) / (4.2 - 3.0) * 100)

# Get battery status
battery_v = get_battery_voltage()
battery_pct = get_battery_percent(battery_v)

# Display scanning status
oled.fill(0)
oled.text(f"Bat: {battery_v:.2f}V", 0, 12)
oled.text(f"     {battery_pct}%", 0, 24)
oled.show()


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

scan_results = wlan.scan()

nets = []

for ap in scan_results:
    ssid_bytes, bssid_bytes, channel, rssi, authmode, hidden = ap

    ssid = ssid_bytes.decode('utf-8') if ssid_bytes else ""

    bssid = ':'.join('{:02x}'.format(b) for b in bssid_bytes)
    nets.append({
        's': ssid,
        'b': bssid,
        'c': channel,
        'r': rssi,
        'a': authmode
    })

ts = int(time.time())

record = {
    'ts': ts,
    'nets': nets
}

try:
    os.mkdir('/scans')
except OSError:
    pass

t = time.localtime()
path = "/scans/%04d-%02d-%02d.jsonl" % (t[0], t[1], t[2])

with open(path, 'a') as f:
    f.write(json.dumps(record) + '\n')

wlan.active(False)
