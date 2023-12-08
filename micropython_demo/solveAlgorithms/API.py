from pololu_3pi_2040_robot import robot
import time

DEFAULT_SPEED_CHANGE = 250
SPEED = 1000
angle_to_turn = 90

class API:
    motors = robot.Motors()
    encoders = robot.Encoders()
    display = robot.Display()

    drive_motors = False
    last_time_gyro_reading = None
    turn_rate = 0.0     # degrees per second
    robot_angle = 0.0   # degrees
    target_angle = 0.0
    last_time_far_from_target = None

    imu = robot.IMU()
    imu.reset()
    imu.enable_default()

    def draw_text(self):
        self.display.fill(0)
        if self.drive_motors:
            self.display.text("A: Stop motors", 0, 0, 1)
            self.display.text("C: Stop motors", 0, 8, 1)
        else:
            self.display.text(f"A: Turn {angle_to_turn} deg", 0, 0, 1)
            self.display.text(f"C: Turn {-angle_to_turn} deg", 0, 8, 1)
        self.display.text(f"Angle:", 0, 32, 1)

    def handle_turn_or_stop(self, angle):
        self.target_angle = self.robot_angle + angle
        drive_motors = not drive_motors
        if drive_motors:
            self.display.fill(1)
            self.display.text("Spinning", 30, 20, 0)
            self.display.text("WATCH OUT", 27, 30, 0)
            self.display.show()
            time.sleep_ms(500)
            self.last_time_far_from_target = time.ticks_ms()
        self.draw_text()
        self.last_time_gyro_reading = time.ticks_us()


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

    def moveForward(self, distance):
        self.encoders.get_counts(reset=True)
        self.motors.set_speeds(SPEED, SPEED)

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
  
    def turnRight(self):
        pass
        

    def turnLeft(self):
        while True:
            self.draw_text()
            # Update the angle and the turn rate.
            if self.imu.gyro.data_ready():
                self.imu.gyro.read()
                self.turn_rate = self.imu.gyro.last_reading_dps[2]  # degrees per second
                now = time.ticks_us()
                if self.last_time_gyro_reading:
                    dt = time.ticks_diff(now, self.last_time_gyro_reading)
                    self.robot_angle += self.turn_rate * dt / 1000000
                self.last_time_gyro_reading = now

                self.handle_turn_or_stop(angle_to_turn)

            # Decide whether to stop the motors.
            if self.drive_motors:
                far_from_target = abs(self.robot_angle - self.target_angle) > 3
                if far_from_target:
                    last_time_far_from_target = time.ticks_ms()
                elif time.ticks_diff(time.ticks_ms(), last_time_far_from_target) > 250:
                    self.drive_motors = False
                    self.draw_text()

            # Show the current angle in degrees.
            self.display.fill_rect(48, 32, 72, 8, 0)
            self.display.text(f"{self.robot_angle - self.target_angle:>9.3f}", 48, 32, 1)
            self.display.show()

            max_speed = 3000
            kp = 140
            kd = 4

            # Drive motors.
            if self.drive_motors:
                turn_speed = (self.target_angle - self.robot_angle) * kp - self.turn_rate * kd
                if turn_speed > max_speed: turn_speed = max_speed
                if turn_speed < -max_speed: turn_speed = -max_speed
                self.motors.set_speeds(-turn_speed, turn_speed)
            else:
                self.motors.off()

    def setWall(x, y, direction):
        pass #command(args=["setWall", x, y, direction])

