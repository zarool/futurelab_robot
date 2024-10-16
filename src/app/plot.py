import math
import numpy as np
import matplotlib.pyplot as plt

from robot.matrics import *
#compute_end_pos, T1, T2, T3, T4, T5

class Plot:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.rx = 0
        self.ry = 0
        self.rz = 0
        
        self.plot_robot(math.pi, -math.pi/2, 0, 0)

        
    def plot_robot(self, theta1, theta2, theta3, theta4):
        a3 = 152.794
        a4 = 157.76
        a5 = 90

        self.rx, self.ry, self.rz = compute_end_pos(theta1, theta2, theta3, theta4, a3, a4, a5)

        self.ax.cla()

        self.ax.plot([0], [0], [0], 'go', label='Base')

        T1_end = T1(theta1)
        T2_end = np.dot(T1_end, T2(theta2))
        T3_end = np.dot(T2_end, T3(theta3, a3))
        T4_end = np.dot(T3_end, T4(theta4, a4))
        T5_end = np.dot(T4_end, T5(a5))

        points = np.array([
            [0, 0, 0],
            T1_end[:3, 3],
            T2_end[:3, 3],
            T3_end[:3, 3],
            T4_end[:3, 3],
            T5_end[:3, 3]
        ])

        self.ax.plot(points[:, 0], points[:, 1], points[:, 2], 'bo-', label='Links')
        self.ax.plot(self.rx, self.ry, self.rz, 'ro', label='End-Effector')

        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_zlim(-200, 200)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('3D Robot Arm')
        self.ax.legend()



