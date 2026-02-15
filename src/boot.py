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
    """Sync time with NTP server with better error handling"""
    print(f"Time before sync: {time.time()} - {time.localtime()}")
    
    ntptime.host = config.NTP_HOST
    print(f"NTP host: {ntptime.host}")
    
    # Try NTP sync with retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            ntptime.settime()
            print(f"NTP sync attempt {attempt + 1} completed")
            time.sleep(0.1)  # Give it a moment to take effect
            break
        except Exception as e:
            print(f"NTP attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    
    current_time = time.time()
    current_local = time.localtime()
    print(f"Time after sync: {current_time} - {current_local}")
    
    # Sanity check: year should be >= 2024
    # MicroPython's time.localtime() returns (year, month, day, hour, min, sec, weekday, yearday)
    year = current_local[0]
    if year < 2024:
        raise RuntimeError(f"Time sync failed: year is {year}, expected >= 2024")


try:
    wlan = connect_wifi()
    print("WiFi connected:", wlan.ifconfig())

    sync_time()
    print("Time synced successfully!")
    print(f"Current time: {time.localtime()}")

    wlan.active(False)
    print("WiFi disabled")

except Exception as e:
    print("Boot warning:", e)
    print("Continuing in dev mode without guaranteed time.")
    # Print current time anyway for debugging
    print(f"Current time value: {time.time()}")
    print(f"Current localtime: {time.localtime()}")
