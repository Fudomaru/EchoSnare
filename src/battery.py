from machine import ADC, Pin
import time

# GPIO37 controls the battery voltage measurement circuit
# V3.2 boards need HIGH (not LOW!)
adc_ctrl = Pin(37, Pin.OUT)
adc_ctrl.value(1)  # Set HIGH to enable (V3.2 change)
time.sleep(0.1)

# GPIO1 is the battery ADC pin
battery_adc = ADC(Pin(1))
battery_adc.atten(ADC.ATTN_11DB)  # 11dB for full range

# Read
raw = battery_adc.read()
voltage_uv = battery_adc.read_uv()
adc_voltage = voltage_uv / 1000000

# Apply voltage divider: 100+390 = 490, so multiply by 4.9
battery_voltage = adc_voltage * 4.9

print(f"Raw: {raw}")
print(f"ADC voltage: {adc_voltage:.3f}V")
print(f"Battery voltage: {battery_voltage:.2f}V")

# Disable to save power
adc_ctrl.value(0)
