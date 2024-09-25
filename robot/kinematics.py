import math
import numpy as np
from robot.matrics import Matrix

def compute_end_effector_position(theta1, theta2, theta3, theta4, a3=152.794, a4=157.76, a5=90):
    T1_matrix = Matrix.T1(theta1)
    T2_matrix = np.dot(T1_matrix, Matrix.T2(theta2))
    T3_matrix = np.dot(T2_matrix, Matrix.T3(theta3, a3))
    T4_matrix = np.dot(T3_matrix, Matrix.T4(theta4, a4))
    T5_matrix = np.dot(T4_matrix, Matrix.T5(a5))
    
    z1 = T1_matrix[2, 3]
    z2 = T2_matrix[2, 3]
    z3 = T3_matrix[2, 3]
    z4 = T4_matrix[2, 3]
    z5 = T5_matrix[2, 3]
    
    if  z3 <= 0 or z4 <= 0 or z5 <= 0:
        raise ValueError("Jeden z punktów znajduje się poniżej lub na poziomie 0 w osi Z")
    
    return T5_matrix[0, 3], T5_matrix[1, 3], z5




def inverse_kinematics(x, y, z, a2=152.794, a3=157.76, a4=90):
    valid_position = 1
    z = z - 180
    # Calculate theta1 based on x and y coordinates
    if(z<0):
        z = z * -1
    elif(z>0):
        z = z * -1

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
    # if(theta2 < 0):
    #     raise ValueError("Target is out of reach")
    print("theta2:", theta2)

    theta4 = -(theta2 + theta3 + np.pi/2)  

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
        pos2 = int((math.degrees(theta2_1) / 360) * steps_per_revolution * (54/28))
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
    compute_end_effector_position(theta1, theta2, theta3, theta4)

    if(pos3 < 150):
        valid_position = 0
    else:
        valid_position = 1
    if(pos4 < 1024):
        valid_position = 0
    else:
        valid_position = 1

    print("pos",pos1)
    print(pos2)
    print(pos3)
    print(pos4)
    

    return theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4, valid_position