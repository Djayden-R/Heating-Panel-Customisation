"""
Add support for additional hardware components:
0.96 inch serial OLED screen
DHT20 Temperature and Humidity sensor
EC11 Rotary Encoder
DC rocker switch
Solid-State Relay (25 Amp 230 AC)
"""
from machine import I2C, Pin, Encoder
from ssd1306 import SSD1306_I2C # https://github.com/stlehmann/micropython-ssd1306
from dht20 import DHT20 # https://github.com/flrrth/pico-dht20
from rotary_irq_esp import RotaryIRQ # https://github.com/miketeachman/micropython-rotary


"""Code below is from the ssd1306 repository, but has been modified"""
# Code used for finding correct address for devices
i2c = I2C(sda=Pin(8), scl=Pin(9))
i2c.scan()

# Set up device
oled = SSD1306_I2C(128, 32, i2c)

# Example commands
oled.fill(1) # Fill screen fully (0 to clear it fully)
oled.show() # Run after every command

oled.text('Hello', 0, 0)
oled.text('World', 0, 10)
oled.show()


"""Code below is from the pico-dht20 repository, but has been modified"""
dht20 = DHT20(0x38, i2c)

measurements = dht20.measurements
print(f"Temperature: {measurements['t']} °C, humidity: {measurements['rh']} %RH")


"""Rotary encoder code"""
rotary_encoder = RotaryIRQ(pin_num_clk=6, 
              pin_num_dt=5, 
              min_val=0, 
              max_val=30, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
encoder_value = rotary_encoder.value()

encoder_button = Pin(7, Pin.IN, Pin.PULL_UP)
encoder_button_value = encoder_button.value()

"""Switch code"""
switch = Pin(12, Pin.IN, Pin.PULL_UP)
switch_value = switch.value()

"""Relay code"""
relay = Pin(13, Pin.OUT)
relay.on()
relay.off()
