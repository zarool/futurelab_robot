import numpy as np

class Matrix:
    # Define the transformation matrices
    def T1(theta1, d1=0):
        return np.array([
            [np.cos(theta1), -np.sin(theta1), 0, 0],
            [np.sin(theta1), np.cos(theta1), 0, 0],
            [0, 0, 1, d1],
            [0, 0, 0, 1]
        ])

    def T2(theta2):
        return np.array([
            [np.cos(theta2), -np.sin(theta2), 0, 0],
            [0, 0, 1, 0],
            [-np.sin(theta2), -np.cos(theta2), 0, 0],
            [0, 0, 0, 1]
        ])

    def T3(theta3, a3):
        return np.array([
            [np.cos(theta3), -np.sin(theta3), 0, a3],
            [np.sin(theta3), np.cos(theta3), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def T4(theta4, a4):
        return np.array([
            [np.cos(theta4), -np.sin(theta4), 0, a4],
            [np.sin(theta4), np.cos(theta4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def T5(a5):
        return np.array([
            [1, 0, 0, a5],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])