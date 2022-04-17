import time
import board
import rotaryio
import digitalio
import displayio
import busio
import adafruit_ssd1306
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from kmk.kmk_keyboard import KMKKeyboard
from kmk.consts import UnicodeMode
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from adafruit_debouncer import Debouncer

keyboard = KMKKeyboard()
layers = Layers()
encoder_handler = EncoderHandler()
keyboard.modules = [layers,encoder_handler]

displayio.release_displays()
i2c = busio.I2C(board.GP1,board.GP0)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display =adafruit_ssd1306.SSD1306_I2C(128,32,i2c)

print("MagroPad")# ----- Rotary Encoder ---- #


kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)


# ----- Rotary Encoder ---- #
encoder = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
last_position = None
butt = digitalio.DigitalInOut(board.GP9)
butt.direction = digitalio.Direction.INPUT
butt.pull = digitalio.Pull.UP
butt_state = None

# ----- Key setup ----- #
switch_left_in = DigitalInOut(board.GP11)
switch_middle_in = DigitalInOut(board.GP8)
switch_right_in = DigitalInOut(board.GP2)
switch_left_in.pull = Pull.UP
switch_middle_in.pull = Pull.UP
switch_right_in.pull = Pull.UP
switch_left = Debouncer(switch_left_in)
switch_middle = Debouncer(switch_middle_in)
switch_right = Debouncer(switch_right_in)


MEDIA = 1
KEY = 2



map = [
    ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    ConsumerControlCode.PLAY_PAUSE,
    ConsumerControlCode.SCAN_NEXT_TRACK,
    ConsumerControlCode.REWIND,
    ConsumerControlCode.MUTE,
    ConsumerControlCode.FAST_FORWARD,
    ConsumerControlCode.VOLUME_DECREMENT,
    ConsumerControlCode.MUTE,
    ConsumerControlCode.VOLUME_INCREMENT,
    ]



switch_state  = [0,0,0]
title = "Media"

titles = [
          "MEDIA",
          "MEDIA 2",
          "Volume",

         ]





while True:
    switch_left.update()  # Debouncer checks for changes in switch state
    switch_middle.update()
    switch_right.update()

    position = encoder.position
    while position > 2:
        position = 0
    while position < 0:
        position +=3
    post = str(position)


    x = 3 * position
    if x > 9:
        x = 0
    if last_position is None or position != last_position:

        display.fill(0) #clears display after position change
        print(post)
        button_state = None
        #display.fill(0)
        title = titles[position]
        #display.show()
    last_position = position

    if position is 0:
        display.show()
    if position is 1:
        display.show()

    if position is 2:
        display.show()
        #x+=3


    if switch_left.fell:
        cc.send(map[x])
    if switch_middle.fell:
        cc.send(map[(x+1)])
    if switch_right.fell:
        cc.send(map[(x+2)])


    time.sleep(0.01)  # debounce
    #print(x)

    display.text(title,55,10,1)








