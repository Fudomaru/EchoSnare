import network
import time
import json
import os
from machine import Pin
import oled_driver
import battery

# Initialize OLED
oled, vext = oled_driver.init_oled()

# Display scanning status
battery_v, battery_pct = battery.get_battery_status()
oled.fill(0)
oled.text("Scanning WiFi...", 0, 0)
oled.text(f"Bat: {battery_v:.2f}V", 0, 12)
oled.text(f"     {battery_pct}%", 0, 24)
oled.show()

# Perform WiFi scan
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

# Update display with results - read battery again
battery_v, battery_pct = battery.get_battery_status()
oled.fill(0)
oled.text(f"Found: {len(nets)}", 0, 0)
oled.text(f"Bat: {battery_v:.2f}V", 0, 12)
oled.text(f"     {battery_pct}%", 0, 24)
oled.text("Saving...", 0, 36)
oled.show()

# Save to file
ts = int(time.time())
record = {
    'ts': ts,
    'bat_v': battery_v,
    'bat_pct': battery_pct,
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

# Final status - read battery one last time
battery_v, battery_pct = battery.get_battery_status()
oled.fill(0)
oled.text(f"Saved {len(nets)} nets", 0, 0)
oled.text(f"Bat: {battery_v:.2f}V", 0, 12)
oled.text(f"     {battery_pct}%", 0, 24)
oled.text("Done!", 0, 48)
oled.show()

time.sleep(2)

# Clean up
wlan.active(False)
oled_driver.power_off_oled(vext)
