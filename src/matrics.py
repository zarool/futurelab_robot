import numpy as np

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

def compute_end_effector_position(theta1, theta2, theta3, theta4, a3=152.794, a4=157.76, a5=90):
    T = np.dot(T1(theta1), np.dot(T2(theta2), np.dot(T3(theta3, a3), np.dot(T4(theta4, a4), T5(a5)))))
    return T[0, 3], T[1, 3], T[2, 3]
