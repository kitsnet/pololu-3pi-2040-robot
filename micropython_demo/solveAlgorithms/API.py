from pololu_3pi_2040_robot import robot
import time
from tof import SensorInterface

DEFAULT_SPEED_CHANGE = 10
SPEED = 1000
angle_to_turn = 90

class API:
    motors = robot.Motors()
    encoders = robot.Encoders()
    display = robot.Display()
    imu = robot.IMU()
    yellow_led = robot.YellowLED()

    def __init__(self):
        self.kp = 140
        self.kd = 4
        self.max_speed = 3000

        self.drive_motors = False
        self.target_angle = 0.0
        self.last_time_far_from_target = None
        self.last_time_gyro_reading = None
        self.robot_angle = 0.0

    def draw_text(self):
        self.display.fill(0)
        if self.drive_motors:
            self.display.text("A: Stop motors", 0, 0, 1)
        else:
            self.display.text("A: Turn Right", 0, 0, 1)
        self.display.text(f"Angle: {self.robot_angle - self.target_angle:>9.3f}", 0, 32, 1)
        self.display.show()

    def handle_turn_or_stop(self, angle_to_turn):
        self.target_angle = self.robot_angle - angle_to_turn
        self.drive_motors = not self.drive_motors
        if self.drive_motors:
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
        display = robot.Display()
        sensor = SensorInterface()
        distance = sensor.getSensorData(2)
        display.fill(0)
        display.text("Wall front", 0, 0)
        display.text(" Sensor2: " + str(distance), 0, 8)
        display.show()
        if distance < 70:
            return True
        else:
            return False

    def wallRight():
        sensor = SensorInterface()
        display = robot.Display()
        distance = sensor.getSensorData(1)
        display.fill(0)
        display.text("Wall Right", 0, 0)
        display.text(" Sensor1: " + str(distance), 0, 8)
        display.show()
        if distance < 70:
            return True
        else:
            return False

    def wallLeft():
        sensor = SensorInterface()
        display = robot.Display()
        distance = sensor.getSensorData(3)
        display.fill(0)
        display.text("Wall Left", 0, 0)
        display.text(" Sensor3: " + str(distance), 0, 8)
        display.show()

        if distance < 70:
            return True
        else:
            return False

    def moveForward(self):
        self.encoders.get_counts(reset=True)
        speed_left = 620
        speed_right = 570
        self.motors.set_speeds(speed_left, speed_right)
        distance = 230

        left_a, right_a = self.encoders.get_counts()
        left = abs(left_a)
        right = abs(right_a)

        counter = 0
        while left < distance and right < distance:
            counter = counter + 1
            left_a, right_a = self.encoders.get_counts()
            left = abs(left_a)
            right = abs(right_a)
            self.display.fill(0)
            self.display.text(f"L: {left} R: {right}",0,0)
            self.display.show()

            if left < right and counter % 1000 == 0:
                counter = 0
                speed_left += DEFAULT_SPEED_CHANGE
                speed_right -= DEFAULT_SPEED_CHANGE
            elif left > right and counter % 1000 == 0:
                counter = 0
                speed_left -= DEFAULT_SPEED_CHANGE
                speed_right += DEFAULT_SPEED_CHANGE
            
            self.motors.set_speeds(speed_left, speed_right)

            # Check for any obstacles or unexpected conditions
            # if obstacle_detected :
                # stop_robot()
                # break  # Exit the loop in case of an obstacle
            # maybe sleep for short time ? 

        # stop
        self.motors.set_speeds(0, 0)
  
    def turnRight(self, angle_to_turn=90):
        self.target_angle = self.robot_angle - angle_to_turn
        self.drive_motors = True

        self.display.fill(1)
        self.display.text("Spinning", 30, 20, 0)
        self.display.text("WATCH OUT", 27, 30, 0)
        self.display.show()
        time.sleep_ms(500)
        self.last_time_far_from_target = time.ticks_ms()

        self.draw_text()
        self.last_time_gyro_reading = time.ticks_us()

        while self.drive_motors:
            # Update the angle and the turn rate.
            if self.imu.gyro.data_ready():
                self.imu.gyro.read()
                turn_rate = self.imu.gyro.last_reading_dps[2]  # degrees per second
                now = time.ticks_us()
                if self.last_time_gyro_reading:
                    dt = time.ticks_diff(now, self.last_time_gyro_reading)
                    self.robot_angle += turn_rate * dt / 1000000
                self.last_time_gyro_reading = now

            # Decide whether to stop the motors.
            if self.drive_motors:
                far_from_target = abs(self.robot_angle - self.target_angle) > 3
                if far_from_target:
                    self.last_time_far_from_target = time.ticks_ms()
                elif time.ticks_diff(time.ticks_ms(), self.last_time_far_from_target) > 250:
                    self.drive_motors = False
                    self.draw_text()

            # Show the current angle in degrees.
            self.display.fill_rect(48, 32, 72, 8, 0)
            self.display.text(f"{self.robot_angle - self.target_angle:>9.3f}", 48, 32, 1)
            self.display.show()

            # Drive motors.
            if self.drive_motors:
                turn_speed = (self.target_angle - self.robot_angle) * self.kp - turn_rate * self.kd
                if turn_speed > self.max_speed: turn_speed = self.max_speed
                if turn_speed < -self.max_speed: turn_speed = -self.max_speed
                self.motors.set_speeds(-turn_speed, turn_speed)
            else:
                self.motors.off()

            self.yellow_led.value(self.drive_motors)     

    def turnLeft(self):
        pass

    def setWall(x, y, direction):
        pass #command(args=["setWall", x, y, direction])

