import numpy as np # type: ignore
import tkinter as tk
from tkinter import messagebox
import math
import firmware.communication as com
import app.plot

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




def inverse_kinematics(x, y, z, a2=152.794, a3=157.76, a4=90):
    # Calculate theta1 based on x and y coordinates
    theta1 = np.arctan2(y, x)  # This is correct
    print("theta1:", theta1)

    # Project the target point into the plane of the second and third joints
    nx = np.sqrt(x**2 + y**2)
    ny = z - 90

    print("Projected coordinates:")
    print("Nx:", nx)
    print("Ny:", ny)

    # Calculate theta3 using the law of cosines
    cos_theta3 = (nx**2 + ny**2 - a2**2 - a3**2) / (2 * a2 * a3)

    # Check if the value is within the valid range for arccos
    if cos_theta3 < -1 or cos_theta3 > 1:
        raise ValueError("Target is out of reach")

    theta3 = np.arccos(cos_theta3)
    print("theta3:", theta3)

    # Calculate theta2 using the geometric method
    k1 = a2 + a3 * np.cos(theta3)
    k2 = a3 * np.sin(theta3)

    beta = np.arctan2(ny, nx)
    alpha = np.arctan2(k2, k1)

    theta2 = beta - alpha
    print("theta2:", theta2)

    theta4 = -(theta2 + theta3 - np.pi/2)

    print("theta4:", theta4)
    theta1_1 = theta1 + 3.141592653589793
    theta2_1 = theta2 + 3.141592653589793
    theta3_1 = theta3 + 3.141592653589793
    theta4_1 = theta4 + 3.141592653589793


    steps_per_revolution = 4096
    if(theta1_1>0):
        pos1 = int((math.degrees(theta1_1) / 360) * steps_per_revolution)
    # elif(theta1 != 0):
    #     pos1 = int(((math.degrees(theta1) / -360) * 2 * steps_per_revolution) + 2048)
    else:
        pos1 = 0
    if(theta2_1>0):
        pos2 = int((math.degrees(theta2_1) / 360) * steps_per_revolution)
    # elif(theta1 != 0):
    #     pos1 = int(((math.degrees(theta1) / -360) * 2 * steps_per_revolution) + 2048)
    else:
        pos2 = 0
    if(theta3_1>0):
        pos3 = int((math.degrees(theta3_1) / 360) * steps_per_revolution)
    # elif(theta1 != 0):
    #     pos1 = int(((math.degrees(theta1) / -360) * 2 * steps_per_revolution) + 2048)
    else:
        pos3 = 0
    if(theta4_1>0):
        pos4 = int((math.degrees(theta4_1) / 360) * steps_per_revolution)
    # elif(theta1 != 0):
    #     pos1 = int(((math.degrees(theta1) / -360) * 2 * steps_per_revolution) + 2048)
    else:
        pos4 = 0

    print("pos",pos1)
    print(pos2)
    print(pos3)
    print(pos4)


    return theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4
