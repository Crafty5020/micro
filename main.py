import utime
utime.sleep(0.1) # wait for usb


rounds = 15

import machine
import lcd_manager as lm
import button_manager as bm
import buzzer_manager as bum
import ujson
import random
# import lcd_manager as lm

with open("morse_code.json", "r") as f:
    morse_code = ujson.load(f)

letter_list = morse_code

led_blue = machine.Pin(22, machine.Pin.OUT)
led_yello = machine.PWM(machine.Pin(9))
led = machine.Pin("LED", machine.Pin.OUT)

led.value(0)
led_blue.value(0)
led_yello.freq(1000)
led_yello.duty_u16(0)

utime.sleep(0.1)

led.value(1)
led_blue.value(0)
led_yello.duty_u16(0)

utime.sleep(1)

led.value(0)
led_blue.value(1)
led_yello.duty_u16(0)

utime.sleep(1)

led.value(0)
led_blue.value(0)
led_yello.duty_u16(65535)

utime.sleep(1)

led.value(0)
led_blue.value(0)
led_yello.duty_u16(0)

lm.init()

while True:
  led.value(0)
  led_blue.value(0)
  led_yello.duty_u16(0)
  ps = bm.select_ps()
  if ps == 1:
    score = 0
    for r in range(rounds):
      if r / rounds >= 0.75:
        letter : str = random.choice(list(letter_list["sentences"])) # type: ignore
        lm.sentence_word(letter, "sentence")
        player1_comp = 0
        for char in letter:
          if char == " ":
            utime.sleep(0.7)
            continue
          lm.show_morse(char)
          bum.buzzMain(char)
          win = bm.ps_go(char, 1)
          bum.buzzPlayer(1, 0)
          bum.buzzPlayer(2, 0)
          if win == 1:
            player1_comp += 1
          utime.sleep(0.3)
        if player1_comp == len(letter):
          score += 1
      elif r / rounds >= 0.50:
        letter : str = random.choice(list(letter_list["words"])) # type: ignore
        player1_comp = 0
        lm.sentence_word(letter, "word")
        for char in letter:
          lm.show_morse(char)
          bum.buzzMain(char)
          win = bm.ps_go(char, 1)
          bum.buzzPlayer(1, 0)
          bum.buzzPlayer(2, 0)
          if win == 1:
            player1_comp += 1
          utime.sleep(0.3)
        if player1_comp == len(letter):
          score += 1
      else:
        letter : str = random.choice(list(letter_list["letters"])) # type: ignore
        lm.show_morse(letter)
        bum.buzzMain(letter)
        win = bm.ps_go(letter, 1)
        bum.buzzPlayer(1, 0)
        bum.buzzPlayer(2, 0)
        score += win
    lm.p1_score(score, rounds)
  else:
    score_p1 = 0
    score_p2 = 0
    for r in range(rounds):
      if r / rounds >= 0.75:
        letter : str = random.choice(list(letter_list["sentences"])) # type: ignore
        lm.sentence_word(letter, "sentence")
        player1_comp = 0
        player2_comp = 0
        for char in letter:
          if char == " ":
            utime.sleep(0.7)
            continue
          lm.show_morse(char)
          bum.buzzMain(char)
          win = bm.ps_go(char, 2)
          bum.buzzPlayer(1, 0)
          bum.buzzPlayer(2, 0)
          if win == 1:
            player1_comp += 1
          elif win == 2:
            player2_comp += 1
          utime.sleep(0.3)
        if player1_comp > player2_comp:
          score_p1 += 1
        elif player2_comp > player1_comp:
          score_p2 += 1
      elif r / rounds >= 0.50:
        letter : str = random.choice(list(letter_list["words"])) # type: ignore
        lm.sentence_word(letter, "word")
        player1_comp = 0
        player2_comp = 0
        for char in letter:
          lm.show_morse(char)
          bum.buzzMain(char)
          win = bm.ps_go(char, 2)
          bum.buzzPlayer(1, 0)
          bum.buzzPlayer(2, 0)
          if win == 1:
            player1_comp += 1
          elif win == 2:
            player2_comp += 1
          utime.sleep(0.3)
        if player1_comp > player2_comp:
          score_p1 += 1
        elif player2_comp > player1_comp:
          score_p2 += 1
      else:
        letter : str = random.choice(list(letter_list["letters"])) # type: ignore
        lm.show_morse(letter)
        bum.buzzMain(letter)
        win = bm.ps_go(letter, 2)
        bum.buzzPlayer(1, 0)
        bum.buzzPlayer(2, 0)
        if win == 1:
          score_p1 += 1
        elif win == 2:
          score_p2 += 1
    if score_p1 > score_p2:
      led_blue.value(1)
      lm.player_win(1, score_p1, score_p2)
    elif score_p2 > score_p1:
      led_yello.duty_u16(65535)
      lm.player_win(2, score_p1, score_p2)
    else:
      led.value(1)
      lm.player_win(0, score_p1, score_p2)

