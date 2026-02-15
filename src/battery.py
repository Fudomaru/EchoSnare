from machine import Pin, ADC
import time

# Pin definitions
ADC_CTRL_PIN = 37  # Controls battery voltage measurement circuit
BATTERY_ADC_PIN = 1  # ADC input for battery voltage

def get_battery_voltage():

    # Enable battery voltage measurement (HIGH for V3.2 boards)
    adc_ctrl = Pin(ADC_CTRL_PIN, Pin.OUT)
    adc_ctrl.value(1)
    time.sleep(0.01)  # Stabilization delay
    
    # Read ADC
    battery_adc = ADC(Pin(BATTERY_ADC_PIN))
    battery_adc.atten(ADC.ATTN_11DB)  # 0-3.3V range
    
    voltage_uv = battery_adc.read_uv()
    adc_voltage = voltage_uv / 1000000
    
    # Apply voltage divider scaling: (100 + 390) / 100 = 4.9
    battery_voltage = adc_voltage * 4.9
    
    # Disable ADC control to save power
    adc_ctrl.value(0)
    
    return battery_voltage

def get_battery_percent(voltage):
    if voltage >= 4.2:
        return 100
    elif voltage <= 3.0:
        return 0
    else:
        # Linear interpolation between 3.0V and 4.2V
        return int((voltage - 3.0) / (4.2 - 3.0) * 100)

def get_battery_status():
    """
    Convenience function that returns both voltage and percentage
    Returns: (voltage_float, percentage_int)
    """
    voltage = get_battery_voltage()
    percent = get_battery_percent(voltage)
    return voltage, percent

# Test code
if __name__ == "__main__":
    voltage, percent = get_battery_status()
    print(f"Battery: {voltage:.2f}V ({percent}%)")
