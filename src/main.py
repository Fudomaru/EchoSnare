import network
import time
import json
import os

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

date_str = time.strftime('%Y-%m-%d')
path = '/scans/{}.jsonl'.format(date_str)

with open(path, 'a') as f:
    f.write(json.dumps(record) + '\n')

wlan.active(False)
