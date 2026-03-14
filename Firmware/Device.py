from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from dht20 import DHT20
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
from time import sleep

# -----------------------------
# Encoder
# -----------------------------
encoder_value = 20

MIN_TEMP = 5
MAX_TEMP = 30

en_pin_clk = Pin(6, Pin.IN, Pin.PULL_UP)
en_pin_dt = Pin(5, Pin.IN, Pin.PULL_UP)
en_pin_sw = Pin(7, Pin.IN, Pin.PULL_UP)

encoder = RotaryEncoderRP2(
    en_pin_clk,
    en_pin_dt,
    en_pin_sw,
    encoder_step=2,   # helpt tegen overslaan
    half_step=True    # nodig voor veel KY-040 encoders
)

def turn_right():
    global encoder_value
    encoder_value += 1
    if encoder_value > MAX_TEMP:
        encoder_value = MAX_TEMP

def turn_left():
    global encoder_value
    encoder_value -= 1
    if encoder_value < MIN_TEMP:
        encoder_value = MIN_TEMP

encoder.on(RotaryEncoderEvent.TURN_RIGHT, turn_right)
encoder.on(RotaryEncoderEvent.TURN_LEFT, turn_left)
# -----------------------------
# I2C devices
# -----------------------------
i2c = I2C(sda=Pin(8), scl=Pin(9))
oled = SSD1306_I2C(128, 32, i2c)
dht20 = DHT20(0x38, i2c)
# -----------------------------
# Inputs / outputs
# -----------------------------
switch = Pin(4, Pin.IN, Pin.PULL_UP)
relay = Pin(21, Pin.OUT)
# -----------------------------
# Screen
# -----------------------------
def update_screen(set_temp, current_temp, humidity, status_message):
    oled.fill(0)
    oled.text("Thermostat", 0, 0)
    oled.text("Set:", 0, 10)
    oled.text(str(set_temp) + "C", 40, 10)
    oled.text("Now:", 0, 20)
    oled.text(str(round(current_temp,1)) + "C", 40, 20)
    oled.text(status_message, 90, 20)
    oled.show()


# -----------------------------
# Sensor
# -----------------------------
def get_temp_and_humidity():
    measurements = dht20.measurements
    temperature = measurements['t']
    humidity = measurements['rh']
    return temperature, humidity


# -----------------------------
# Main logic
# -----------------------------
HYSTERESIS = 0.3

def main():
    system_on = False
    while True:
        # Let encoder process events
        encoder.raw_tick()

        # SWITCH ON
        if switch.value() == 0:

            if not system_on:
                oled.poweron()
                system_on = True

            current_temperature, humidity = get_temp_and_humidity()
            set_temperature = encoder_value

            if current_temperature < set_temperature - HYSTERESIS:
                relay.on()
                status = "HEAT"

            elif current_temperature > set_temperature + HYSTERESIS:
                relay.off()
                status = "OFF"

            else:
                status = "HEAT" if relay.value() else "OFF"

            update_screen(set_temperature, current_temperature, humidity, status)

            sleep(0.1)

        # SWITCH OFF
        else:
            if system_on:
                relay.off()
                oled.fill(0)
                oled.text("Thermostat", 0, 0)
                oled.text("Turning off...", 0, 16)
                oled.show()
                sleep(2)
                oled.poweroff()
                system_on = False

            sleep(0.1)


if __name__ == "__main__":
    main()
