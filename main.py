import utime
utime.sleep(0.1) # wait for usb


rounds = 15

import machine
import button_manager as bm
import buzzer_manager as bum
import ujson
import random
# import lcd_manager as lm

with open("morse_code.json", "r") as f:
    morse_code = ujson.load(f)

letter_list = list(morse_code.keys())

led_blue = machine.Pin(22, machine.Pin.OUT)
led_yello = machine.Pin(9, machine.Pin.OUT)
led = machine.Pin("LED", machine.Pin.OUT)

led.value(0)
led_blue.value(0)
led_yello.value(0)

utime.sleep(0.1)

led.value(1)
led_blue.value(0)
led_yello.value(0)

utime.sleep(1)

led.value(0)
led_blue .value(0)
led_yello.value(1)

utime.sleep(1)

led.value(0)
led_blue.value(1)
led_yello.value(0)

utime.sleep(1)

led.value(0)
led_blue.value(0)
led_yello.value(0)

# lm.init()

while True:
  ps = bm.select_ps()
  if ps == 1:
    score = 0
    for round in range(1,rounds):
      letter : str = random.choice(letter_list) # type: ignore
      # lm.show_morse(letter)
      win = bm.ps_go(letter, 1)
      score += win
    # lm.p1_score(score, rounds)
  else:
    score_p1 = 0
    score_p2 = 0
    for round in range(1,rounds):
      letter : str = random.choice(letter_list) # type: ignore
      # lm.show_morse(letter)
      win = bm.ps_go(letter, 2)
      if win == 1:
        score_p1 += 1
      elif win == 2:
        score_p2 += 1
    if score_p1 > score_p2:
      pass
      # lm.player_win(1)
    elif score_p2 > score_p1:
      pass
      # lm.player_win(2)
    else:
      pass
      # lm.player_win(0)


