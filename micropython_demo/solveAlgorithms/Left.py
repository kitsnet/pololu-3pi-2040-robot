import API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

log("Running...")
#API.setColor(0, 0, "G")
#API.setText(0, 0, "abc")
while True:
    if not API.wallLeft():
        API.turnLeft()
    while API.wallFront():
        API.turnRight()
    API.moveForward()
