import sys

class MouseCrashedError(Exception):
    pass


def mazeWidth():
    return 16 #command(args=["mazeWidth"], return_type=int)

def mazeHeight():
    return 16 #command(args=["mazeHeight"], return_type=int)

def wallFront():
    return False #command(args=["wallFront"], return_type=bool)

def wallRight():
    return False #command(args=["wallRight"], return_type=bool)

def wallLeft():
    return False #command(args=["wallLeft"], return_type=bool)

def moveForward():
    pass
    #response = command(args=["moveForward"], return_type=str)
    #if response == "crash":
    #    raise MouseCrashedError()

def turnRight():
    pass #command(args=["turnRight"], return_type=str)

def turnLeft():
    pass #command(args=["turnLeft"], return_type=str)

def setWall(x, y, direction):
    pass #command(args=["setWall", x, y, direction])

