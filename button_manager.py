from machine import Pin
import ujson
from utime import sleep, ticks_ms, ticks_diff
import buzzer_manager as bum

p1_button = Pin(10, Pin.IN, Pin.PULL_UP)
p2_button = Pin(2, Pin.IN, Pin.PULL_UP)
wpm = 12
last_state = {1: 1, 2: 1}     # initial unpressed
press_time = {1: 0, 2: 0}
with open("morse_code.json", "r") as f:
    morse_code = ujson.load(f)
morse_code = {letter: bytearray(vals) for letter, vals in morse_code.items()}
DIT_MS = int(1200 / wpm)
DAH_THRESHOLD = DIT_MS * 2


def select_ps():
    while True:
        if p1_button.value() == 0:
            return 1
        elif p2_button.value() == 0:
            return 2

def ps_go(letter, players):
    p1_morse = bytearray()
    p2_morse = bytearray()
    round_start = ticks_ms()
    while True:
        print(p1_morse)
        p2 = None
        p1 = poll_morse(p1_button, 1)
        if players == 2:
            p2 = poll_morse(p2_button, 2)

        if p1 is not None:
            p1_morse.append(p1)
        if p2 is not None and players == 2:
            p2_morse.append(p2)
        
        if players == 2:
            if p1_morse == morse_code[letter]:
                return 1
            if p2_morse == morse_code[letter]:
                return 2
        if players == 1:
            if p1_morse == morse_code[letter]:
                return 1

        if ticks_diff(ticks_ms(), round_start) / 1000 >= 3:
            return 0
        sleep(0.005)


          

def poll_morse(button, player):

    global last_state
    global press_time

    state = button.value()

    # button just pressed
    if last_state[player] == 1 and state == 0:
        bum.buzzPlayer(player, 1)
        press_time[player] = ticks_ms()
    # button just released
    elif last_state[player] == 0 and state == 1:
        bum.buzzPlayer(player, 0)
        held = ticks_diff(ticks_ms(), press_time[player])

        last_state[player] = state  # update before returning

        if held < DAH_THRESHOLD:
            return 0x00  # dit
        elif held < 5 * int((1200/wpm)):        # optional max limit to reject extremely long presses
            return 0x01  # dah
        else:
            return None  # ignore too long

    last_state[player] = state
    return None
