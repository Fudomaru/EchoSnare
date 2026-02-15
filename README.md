# ESP32-S3 Projekt

## Why?

I don't think I really need a reason except 
that learning is fun, and if I really want to 
understand Software, Infrastructure, Tools, and everything in between, 
I have to work with some hardware I can configure from the core up. 

After looking around, my decision went to the ESP32. 
And that is the whole reason. 

## What? 

Here is a link to my first general thoughts of what I am trying to build:

[EchoSnare](https://voidex.me/projects/echosnare/)

In general I decided to try to build a WiFi sniffer
and see what happens. 
My hope is that I will learn a lot about 
how our wireless networks actually work, what you can do with it,
and especially important for me: 
What Security with networks over the air really means.

## Current Progress

### Hardware
- **Board:** Heltec WiFi LoRa 32 V3
  - ESP32-S3FN8 microcontroller
  - SX1262 LoRa transceiver (not using yet)
  - 0.96" OLED display (128x64, SSD1306)
  - Built-in battery management
- **Firmware:** MicroPython v1.27.0 (ESP32S3 generic)

### What's Working

**Network Scanner** (`main.py`)
- Scans for WiFi networks and captures:
  - SSID (network name)
  - BSSID (MAC address)
  - Channel
  - Signal strength (RSSI)
  - Authentication mode
- Logs everything to daily JSONL files in `/scans/`
- Includes timestamp and battery status with each scan

**Time Synchronization** (`boot.py`)
- Connects to WiFi on startup
- Syncs time via NTP (using `de.pool.ntp.org`)
- Validates sync worked (checks year >= 2024)
- Disconnects WiFi to save battery after sync
- Has retry logic because networks can be flaky

**Battery Monitoring** (`battery.py`)
- Reads LiPo battery voltage via ADC
- Converts to percentage (4.2V = 100%, 3.0V = 0%)
- Logs battery data with each scan to track power consumption

**OLED Display** (`oled_driver.py`)
- Shows scan status in real-time:
  - "Scanning WiFi..."
  - Number of networks found
  - Battery voltage and percentage
  - "Saving..." and "Done!" status
- Powers off after scan to save battery
- Took way too long to figure out the correct initialization sequence

### File Structure

```
/
├── ssd1306.py       - Standard OLED driver (Adafruit)
├── oled_driver.py   - Heltec V3-specific OLED init (Vext power, reset, pins)
├── battery.py       - Battery voltage reading (GPIO1 ADC with voltage divider)
├── boot.py          - Startup: WiFi + NTP time sync
├── main.py          - Main scanner loop with OLED feedback
└── config.py        - WiFi credentials and NTP host (not in repo)
```

### Hardware Notes (for future me)

**OLED (SSD1306):**
- **Vext (GPIO36):** Must be LOW to power the OLED panel
- **RST (GPIO21):** Reset pin (pulse LOW then HIGH)
- **SDA (GPIO17), SCL (GPIO18):** I2C communication
- **I2C Speed:** 50kHz (400kHz causes timeouts)
- The OLED controller responds to I2C even without Vext, but pixels won't light up

**Battery:**
- **ADC_CTRL (GPIO37):** Must be HIGH on V3.2 boards (was LOW on older versions)
- **Battery ADC (GPIO1):** Reads voltage through 100Ω/390Ω divider
- Formula: `VBAT = ADC_voltage × 4.9`
- Use `ADC.ATTN_11DB` for 0-3.3V range

**Power:**
- Alive LED on GPIO35 (currently always on, should probably turn this off to save power)
- LoRa not initialized yet (future feature)

## What's Next

- Get automatic Repetition every x Minutes to get more regular data
- Maybe add deep sleep between scans for longer battery life
- Build some kind of data analysis tool for the scan logs
- Learn more about what you can actually do with WiFi packet data
- Security implications of all this

## Lessons Learned

1. **Hardware documentation lies sometimes.** The Meshtastic docs said GPIO41/42 for I2C. Actually GPIO17/18. Spent way too long on this.

2. **I2C speed matters.** 400kHz timed out, 50kHz works. Sometimes slower is better.

3. **Power control is invisible but critical.** The OLED responded to I2C but wouldn't display anything until I enabled Vext. An hour of debugging for one line of code.

4. **MicroPython uses 2000 as epoch, not 1970.** This broke my time sanity checks initially.

5. **Battery voltage needs circuit enable.** Can't just read GPIO1 directly—need to enable the measurement circuit first via GPIO37.

6. **Debugging hardware is humbling.** You think you're stupid, but really the problem is just invisible. Keep testing systematically.

## Conclusion

Still work in progress, but now it actually does something useful.
The scanner works, the display works, time sync works, battery monitoring works.
Next step: figure out what to do with all this WiFi data I'm collecting.
