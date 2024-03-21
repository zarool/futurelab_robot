from math import pi, sin, cos
import numpy as np

# suppress big decimals
# np.set_printoptions(precision=4, suppress=True)
np.set_printoptions(formatter={'float': '{: 0.4f}'.format})


class Robot:
    def __init__(self, theta, lamb, length, alpha):
        self.theta = np.array(theta)
        self.lamb = np.array(lamb)
        self.length = np.array(length)
        self.alpha = np.array(alpha)

        self.vector = np.zeros((4, 4))
        self.pos = np.zeros((1, 3))

        # calculate position
        self.position()

    @staticmethod
    def matrix_a(theta, lamb, length, alpha):
        return (
            [cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), length * cos(theta)],
            [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), length * sin(theta)],
            [0, sin(alpha), cos(alpha), lamb],
            [0, 0, 0, 1])

    def position(self):
        temp = []
        for i in range(3):
            temp.append(self.matrix_a(self.theta[i], self.lamb[i], self.length[i], self.alpha[i]))

        temp1 = np.dot(temp[0], temp[1])
        self.vector = np.dot(temp1, temp[2])
        self.pos = self.vector[:3, 3]
        return self.pos

    def __str__(self):
        string = (f"Manipulator \n"
                  f"===================\n"
                  f"Podstawowe dane:\n"
                  f"Theta:  {self.theta}\n"
                  f"Lambda: {self.lamb}\n"
                  f"L:      {self.length}\n"
                  f"Alpha:  {self.alpha}\n"
                  f"===================\n"
                  f"Wektor pozycji i macierz orientacji \n"
                  f"{self.vector}\n"
                  f"===================\n"
                  f"Aktualna pozycja: (x, y, z)\n"
                  f"{self.pos}\n")

        return string
