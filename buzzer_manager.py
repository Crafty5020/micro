from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
import ujson

p1_buz = Pin(8, Pin.OUT)
p2_buz = Pin(17, Pin.OUT)
main_buz = Pin(21, Pin.OUT)
with open("morse_code.json", "r") as f:
    morse_code = ujson.load(f)
wpm = 12


def buzzMain(letter):
    duration = 0.100
    letter = letter.upper()

    for morse in morse_code[letter]:
        if morse == 0:
            duration = 1.2 / wpm
        else:
            duration = (1.2 / wpm) * 3

        main_buz.value(1)
        sleep(duration)
        main_buz.value(0)
        sleep(1.2 / wpm)

def buzzPlayer(player, pressed):
    if player == 1:
        p1_buz.value(pressed)
    else:
        p2_buz.value(pressed)


