from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from gpiozero import Button
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--stop", action="store_true", help="Stop switch")


def get_cpu_temp():
    tmp = open("/sys/class/thermal/thermal_zone0/temp")
    cpu = tmp.read()
    tmp.close()
    return "{:.2f}".format(float(cpu) / 1000) + " C"


fan_level = -1


def get_fan_level():
    tmp = open("/sys/class/thermal/cooling_device0/cur_state")
    fan = tmp.read()
    tmp.close()
    global fan_level
    fan_level = int(fan)


def set_fan_level(level):
    if level < 0:
        level = 0
    if level > 4:
        level = 4
    tmp = open("/sys/class/thermal/cooling_device0/cur_state", "w")
    tmp.write(str(level))
    tmp.close()


def loop():
    mcp.output(3, 1)
    lcd.begin(16, 2)
    while True:
        get_fan_level()
        lcd.setCursor(0, 0)
        lcd.message("CPU: " + get_cpu_temp() + "\n")
        lcd.message("FAN: " + str(fan_level))

        sleep(1)


def destroy():
    lcd.clear()


PCF8574_address = 0x27
PCF8574A_address = 0x3F

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except IOError:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except IOError:
        print("I2C Address Error !")
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)


up_button = Button("BOARD38")
down_button = Button("BOARD40")


up_button.when_pressed = lambda: set_fan_level(fan_level + 1)
down_button.when_pressed = lambda: set_fan_level(fan_level - 1)

args = parser.parse_args()
if args.stop:
    set_fan_level(0)
    lcd.clear()
else:
    print("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
