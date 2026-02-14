import gc
import network
import time
import ntptime
import config

gc.enable()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

    timeout = 10
    start = time.time()

    while not wlan.isconnected():
        if time.time() - start > timeout:
            raise RuntimeError("WiFi connection timeout")
        time.sleep(0.5)

    return wlan


def sync_time():
    ntptime.host = config.NTP_HOST
    ntptime.settime()

    # basic sanity check (epoch > ~2023)
    if time.time() < 1700000000:
        raise RuntimeError("Time sync failed")


try:
    wlan = connect_wifi()
    print("WiFi connected:", wlan.ifconfig())

    sync_time()
    print("Time synced:", time.localtime())

    wlan.active(False)
    print("WiFi disabled")

except Exception as e:
    print("Boot warning:", e)
    print("Continuing in dev mode without guaranteed time.")
