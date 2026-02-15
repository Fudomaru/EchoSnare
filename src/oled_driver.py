"""
OLED Display Driver for Heltec WiFi LoRa 32 V3
Properly initializes the SSD1306 OLED with correct power and reset sequence
"""

from machine import Pin, I2C
import ssd1306
import time

# Pin definitions for Heltec V3
VEXT_PIN = 36   # External peripheral power control (active LOW)
RST_PIN = 21    # OLED reset
SDA_PIN = 17    # I2C data
SCL_PIN = 18    # I2C clock
I2C_FREQ = 50000  # 50kHz - slow but reliable

def init_oled():
    """Initialize the OLED display with proper power sequence"""
    
    # Step 1: Enable Vext (power to OLED panel)
    vext = Pin(VEXT_PIN, Pin.OUT)
    vext.value(0)  # Active LOW to enable
    time.sleep(0.2)
    
    # Step 2: Reset OLED controller
    rst = Pin(RST_PIN, Pin.OUT)
    rst.value(0)  # Pull LOW
    time.sleep(0.1)
    rst.value(1)  # Release HIGH
    time.sleep(0.1)
    
    # Step 3: Initialize I2C
    i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=I2C_FREQ)
    
    # Step 4: Create OLED object
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
    
    # Step 5: Set maximum contrast for visibility
    oled.contrast(255)
    
    # Step 6: Clear display
    oled.fill(0)
    oled.show()
    
    return oled, vext

def power_off_oled(vext):
    """Disable OLED power to save battery"""
    vext.value(1)  # Active LOW, so HIGH = off

# Example usage:
if __name__ == "__main__":
    print("Initializing OLED...")
    oled, vext = init_oled()
    
    print("Displaying test message...")
    oled.text("System", 0, 0)
    oled.text("OLED Ready", 0, 12)
    oled.show()
    
    print("OLED initialized successfully!")
