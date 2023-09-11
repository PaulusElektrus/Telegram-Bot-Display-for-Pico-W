from config import utelegram_config
from config import wifi_config

import utelegram
import network

from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
from time import sleep

# using default address 0x3C
i2c = SoftI2C(sda=Pin(4), scl=Pin(5))
display = SSD1306_I2C(128, 64, i2c)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect(wifi_config['ssid'], wifi_config['password'])

def get_message(message):
    bot.send(message['message']['chat']['id'], message['message']['text'].upper())

def reply_ping(message):
    print(message)
    bot.send(message['message']['chat']['id'], 'pong')

def display_text(message):
    display.fill(0)
    text = message['message']['text']
    text = text.lstrip("/text ")
    segment_size = 16
    leer_size = 12
    line = 0
    current = ""
    for char in text:
        current += char
        if len(current) >= leer_size and char ==" ":
            display.text(current, 0, line, 1)
            line += 12
            current = ""
        elif len(current) == segment_size:
            display.text(current, 0, line, 1)
            line += 12
            current = ""
    if current:
        display.text(current, 0, line, 1)
    display.show()
    bot.send(message['message']['chat']['id'], 'OK')

if sta_if.isconnected():
    bot = utelegram.ubot(utelegram_config['token'])
    bot.register('/ping', reply_ping)
    bot.register('/text', display_text)
    bot.set_default_handler(get_message)

    print('BOT LISTENING')
    bot.listen()
else:
    print('NOT CONNECTED - aborting')


