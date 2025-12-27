from machine import I2C, Pin, Encoder
from ssd1306 import SSD1306_I2C # https://github.com/stlehmann/micropython-ssd1306
from dht20 import DHT20 # https://github.com/flrrth/pico-dht20
from rotary_irq_esp import RotaryIRQ # https://github.com/miketeachman/micropython-rotary
from time import sleep


"""Code below is from the ssd1306 repository, but has been modified"""
# Code used for finding correct address for devices
i2c = I2C(sda=Pin(8), scl=Pin(9))
i2c.scan()

# Set up LCD
oled = SSD1306_I2C(128, 32, i2c)

dht20 = DHT20(0x38, i2c)

def set_screen():
    """Example screen commands"""
    oled.fill(1) # Fill screen fully (0 to clear it fully)
    oled.show() # Run after every command

    oled.text('Hello', 0, 0)
    oled.text('World', 0, 10)
    oled.show()

def update_screen(set_temp, current_temp, status_message):
    pass



def get_temp_and_humidity():
    measurements = dht20.measurements
    temperature = measurements['t']
    humidity = measurements['rh']
    return temperature, humidity


"""Rotary encoder code"""
rotary_encoder = RotaryIRQ(pin_num_clk=6, 
              pin_num_dt=5, 
              min_val=0, 
              max_val=30, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP
            )

encoder_button = Pin(7, Pin.IN, Pin.PULL_UP)
encoder_button_value = encoder_button.value()

switch = Pin(12, Pin.IN, Pin.PULL_UP)

relay = Pin(13, Pin.OUT)

def main():
    while True:
        if switch.value() == 1 # if device is switched on
            set_screen()
            current_temperature, humidity = get_temp_and_humidity()

            set_temperature = rotary_encoder.value()

            if current_temperature < set_temperature:
                if relay.value() != 1:
                    relay.on()
            else:
                if relay.value() == 1:
                    relay.off()

            update_screen(set_temperature, current_temperature)

        else:
            sleep(0.1)

if __name__ == "__main__":
    main()
