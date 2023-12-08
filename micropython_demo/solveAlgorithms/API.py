from pololu_3pi_2040_robot import robot
import time
from tof import SensorInterface

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
        global target_angle, drive_motors
        global last_time_far_from_target, last_time_gyro_reading
        target_angle = self.robot_angle + angle
        drive_motors = not drive_motors
        if drive_motors:
            self.display.fill(1)
            self.display.text("Spinning", 30, 20, 0)
            self.display.text("WATCH OUT", 27, 30, 0)
            self.display.show()
            time.sleep_ms(500)
            last_time_far_from_target = time.ticks_ms()
        self.draw_text()
        last_time_gyro_reading = time.ticks_us()


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
        self.draw_text()
        # Update the angle and the turn rate.
        if self.imu.gyro.data_ready():
            self.imu.gyro.read()
            turn_rate = self.imu.gyro.last_reading_dps[2]  # degrees per second
            now = time.ticks_us()
            if last_time_gyro_reading:
                dt = time.ticks_diff(now, last_time_gyro_reading)
                robot_angle += turn_rate * dt / 1000000
            last_time_gyro_reading = now

            self.handle_turn_or_stop(angle_to_turn)

        # Decide whether to stop the motors.
        if drive_motors:
            far_from_target = abs(robot_angle - target_angle) > 3
            if far_from_target:
                last_time_far_from_target = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), last_time_far_from_target) > 250:
                drive_motors = False
                self.draw_text()

        # Show the current angle in degrees.
        self.display.fill_rect(48, 32, 72, 8, 0)
        self.display.text(f"{robot_angle - target_angle:>9.3f}", 48, 32, 1)
        self.display.show()

        # Drive motors.
        if drive_motors:
            turn_speed = (target_angle - robot_angle) * 140 - turn_rate * 4
            if turn_speed > 3000: turn_speed = 3000
            if turn_speed < -3000: turn_speed = -3000
            self.motors.set_speeds(-turn_speed, turn_speed)
        else:
            self.motors.off()

    def setWall(x, y, direction):
        pass #command(args=["setWall", x, y, direction])

