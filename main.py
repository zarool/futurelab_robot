from app.Window import Window

from robot.Robot import Robot

# ROBOT CONFIGURATION PARAMETERS
theta = [0, 30, 50]  # [deg]
lambd = [0, 0, 0]  # [m]
length = [0.4, 1, 1]  # [m]
alpha = [0, 0, 0]  # [rad]
robot = Robot(theta, lambd, length, alpha)

# RUN WINDOW
app = Window("Test", 500, 500)

# SCRIPT
# print(robot)

app.update(robot.theta, robot.length)
app.run()

