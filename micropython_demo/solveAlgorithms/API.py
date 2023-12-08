import sys
from pololu_3pi_2040_robot import robot

DEFAULT_SPEED_CHANGE = 250

class MouseCrashedError(Exception):
    pass

class ControlMovement:
    motors = robot.Motors()
    encoders = robot.Encoders()

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

    def moveForward(self, speed_left, speed_right, distance):
        self.encoders.get_counts(reset=True)
        self.motors.set_speeds(speed_left, speed_right)

        left, right = self.encoders.get_counts()

        while left < distance and right < distance:
            left, right = self.encoders.get_counts()
            print("Left value: {left}")
            print("Right value: {right}")

            if left < right:
                speed_left += DEFAULT_SPEED_CHANGE
                speed_right -= DEFAULT_SPEED_CHANGE
            else:
                speed_left -= DEFAULT_SPEED_CHANGE
                speed_right += DEFAULT_SPEED_CHANGE
            
            self.motors.set_speed(speed_left, speed_right)

            # Check for any obstacles or unexpected conditions
            # if obstacle_detected :
                # stop_robot()
                # break  # Exit the loop in case of an obstacle
            # maybe sleep for short time ? 

        # stop
        self.motors.set_speeds(0, 0)
  
    def turnRight(self, speed_left, speed_right):
        self.motors.set_speeds(speed_left, -speed_right)

        # Calculate the duration for the rotation
        # rotation_time = abs(90) * 0.011  # Adjust this multiplier based on experimentation
        # time.sleep(rotation_time)

    def turnLeft(self, speed_left, speed_right):
        self.motors.set_speeds(-speed_left, speed_right)

        # Calculate the duration for the rotation
        # rotation_time = abs(90) * 0.011  # Adjust this multiplier based on experimentation
        # time.sleep(rotation_time)

    def setWall(x, y, direction):
        pass #command(args=["setWall", x, y, direction])

