from robot.kinematics import inverse_kinematics

from robot.matrices import *

class Robot:
    def __init__(self) -> None:
        pass

    def update_robot(self, x, y, z):
        try:
            theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4, valid_position = inverse_kinematics(x, y, z)

            if theta1 is not None:
                return theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4
        except ValueError:
            print("ValueError")

        return 0, 0, 0, 0, 0, 0, 0, 0,
