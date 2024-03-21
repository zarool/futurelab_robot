from app.Window import Window
from robot.Graph import Graph
from robot.Robot import Robot

# ROBOT CONFIGURATION PARAMETERS
theta = [30, 1.5, 0]  # [rad]
lambd = [0, 1, 1]  # [m]
length = [1, 1, 0]  # [m]
alpha = [3 / 2 * 3.14, 0, 0]  # [rad]
robot = Robot(theta, lambd, length, alpha)

print(robot)

# window class with tkinter usage
window = Window("Test", 500, 500)

# graph class for showing 3D graph and visualizing robot movement
graph = Graph()

graph.plot_graph(window.root)
window.run()
