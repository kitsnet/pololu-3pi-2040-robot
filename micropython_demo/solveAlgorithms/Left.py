import API
import sys
from pololu_3pi_2040_robot import robot

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def playMusic():
    final_countdown = "!L16 V8 c<bc4<f4 r d16c16d8c8<b4 r d16c16d4<f4 r <b16<a16<b8<a8<f8<b8 r"
    buzzer = robot.Buzzer()
    buzzer.play_in_background(final_countdown)

playMusic()
display = robot.Display()
display.text("Running...", 0,0)
#API.setColor(0, 0, "G")
#API.setText(0, 0, "abc")
while True:
    if not API.wallLeft():
        API.turnLeft()
    while API.wallFront():
        API.turnRight()
    API.moveForward()
