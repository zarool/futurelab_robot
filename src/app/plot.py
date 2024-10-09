import math

def plot_robot(theta1, theta2, theta3, theta4):
    global ax, coordinates_label

    a3 = 152.794
    a4 = 157.76
    a5 = 90

    rx, ry, rz = k.compute_end_effector_position(theta1, theta2, theta3, theta4, a3, a4, a5)

    ax.cla()

    ax.plot([0], [0], [0], 'go', label='Base')

    T1_end = k.T1(theta1)
    T2_end = np.dot(T1_end, k.T2(theta2))
    T3_end = np.dot(T2_end, k.T3(theta3, a3))
    T4_end = np.dot(T3_end, k.T4(theta4, a4))
    T5_end = np.dot(T4_end, k.T5(a5))

    points = np.array([
        [0, 0, 0],
        T1_end[:3, 3],
        T2_end[:3, 3],
        T3_end[:3, 3],
        T4_end[:3, 3],
        T5_end[:3, 3]
    ])

    ax.plot(points[:, 0], points[:, 1], points[:, 2], 'bo-', label='Links')
    ax.plot(rx, ry, rz, 'ro', label='End-Effector')

    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_zlim(-200, 200)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Robot Arm')
    ax.legend()

    coordinates_label.configure(text=f"End-Effector Coordinates:\nX: {rx:.2f}, Y: {ry:.2f}, Z: {rz:.2f}")

def init_plot():
    global fig, ax
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    plot_robot(math.pi, -math.pi/2, 0, 0)

def update_display(servo_id, voltage, current, temperature, pos, load):
    data = (servo_id, f"{voltage:.1f}V", f"{current:.1f}A", f"{temperature:.1f}C", pos, f"{load:.1f}N")
    table.insert_or_update(servo_id, values=data)