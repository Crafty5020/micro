import machine
import utime
import ujson
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

with open("morse_code.json", "r") as f:
    morse_code = ujson.load(f)
morseBYTES_code = {letter: bytearray(vals) for letter, vals in morse_code["letters"].items()}
dit_hex = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x0E, 0x04])
dah_hex = bytearray([0x00, 0x00, 0x00, 0x1F, 0x1F, 0x00, 0x00, 0x00])
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()

lcd.custom_char(0,dit_hex)
lcd.custom_char(1,dah_hex)

lcd.display_on()
lcd.backlight_on()
lcd.blink_cursor_off()
lcd.hide_cursor()

def player_win(player, score1, score2):
    global lcd
    lcd.clear()
    if player != 0:
        lcd.move_to(4,0)
        lcd.putstr(f"Player {player}")
        lcd.move_to(4,1)
        lcd.putstr("Winner!")
    elif score1 == score2 and score1 + score2 != 0:
        lcd.move_to(5,0)
        lcd.putstr(f"It's a")
        lcd.move_to(4,1)
        lcd.putstr("Draw!")
    else:
        lcd.move_to(3, 0)
        lcd.putstr(f"Both Lost!")
    utime.sleep(3.5)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("1P press P1_but")
    lcd.move_to(0,1)
    lcd.putstr("2Ps press P2_but")

def sentence_word(string, type):
    global lcd
    lcd.clear()
    if type == "sentence":
        lcd.move_to(0,0)
        lcd.putstr("Sentence:")
    else:
        lcd.move_to(0,0)
        lcd.putstr("Word:")
    lcd.move_to(0,1)
    lcd.putstr(f"{string}")
    utime.sleep(1.5)
def p1_score(score, rounds):
    global lcd
    lcd.clear()
    lcd.move_to(4,0)
    lcd.putstr(f"{score}/{rounds}!")
    if score/rounds <= 0.25:
        lcd.move_to(4,1)
        lcd.putstr(f"You lost")
    elif score/rounds > 0.25 and score/rounds <= 0.50:
        lcd.move_to(0,1)
        lcd.putstr(f"Alr you did good!")
    elif score/rounds > 0.50 and score/rounds <= 0.75:
        lcd.move_to(1,1)
        lcd.putstr(f"Getting Better")
    elif score/rounds > 0.75 and score/rounds < 1:
        lcd.move_to(1,1)
        lcd.putstr(f"Almost perfect")
    elif score/rounds == 1:
        lcd.move_to(3,1)
        lcd.putstr(f"Perfection")
    utime.sleep(3.5)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("1P press P1_but")
    lcd.move_to(0,1)
    lcd.putstr("2Ps press P2_but")

def show_countdown(number):
    global lcd
    lcd.clear()
    lcd.move_to(7,0)
    lcd.putstr(f"{number}!")
def show_morse(char):
    global lcd
    lcd.clear()
    char = char.upper()
    morse = morse_code["letters"][char]
    lcd.putstr(f"{str(char)}")
    lcd.move_to(2,0)
    for sound in morse:
        lcd.putchar(chr(0) if sound == 0 else chr(1))
        utime.sleep(0.1)
def init():
    global lcd
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Morse Game")
    utime.sleep(2.5)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("1P press P1_but")
    lcd.move_to(0,1)
    lcd.putstr("2Ps press P2_but")



def ps2(ps):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(f"{ps} players select")
    lcd.move_to(3,1)
    lcd.putstr("Get ready!")

