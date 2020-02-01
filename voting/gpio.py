from gpiozero import Button
from time import sleep


button1 = Button(2)
button2 = Button(2)

def check_button_state():
    while True:
        if button1.is_pressed:
            return 1
        elif button2.is_pressed:
            return 2
        else:
            sleep(1)
