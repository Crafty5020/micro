from machine import PWM, Pin
from utime import sleep, ticks_ms, ticks_diff
import ujson

p1_buz = PWM(Pin(28))
p2_buz = PWM(Pin(8))
main_buz = PWM(Pin(16))
with open("morse_code.json", "r") as f:
    morse_code = ujson.load(f)
wpm = 12
p1_buz.freq(1000)
p2_buz.freq(1000)
main_buz.freq(1000)

def buzzMain(letter):
    duration = 0.100
    letter = letter.upper()

    for morse in morse_code["letters"][letter]:
        if morse == 0:
            duration = 1.2 / wpm
        else:
            duration = (1.2 / wpm) * 3

        main_buz.duty_u16(12000)
        sleep(duration)
        main_buz.duty_u16(0)
        sleep(1.2 / wpm)

def buzzPlayer(player, pressed):
    if player == 1:
        p1_buz.duty_u16(12000 if pressed else 0)
    else:
        p2_buz.duty_u16(12000 if pressed else 0)


