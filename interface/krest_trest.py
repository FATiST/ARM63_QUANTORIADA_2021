import numpy as np
import matplotlib.pyplot as plt
import math
import time
import telnetlib
import random
# Robot Link Length Parameter
link = [20, 19]
# Robot Initial Joint Values (degree)
angle = [0, 0, 0, 0]
# Target End of Effector Position
target = [0, 0, 0]

# Create figure to plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


# Draw Axis
def draw_axis(ax, scale=1.0, A=np.eye(4), style='-', draw_2d=False):
    xaxis = np.array([[0, 0, 0, 1],
                      [scale, 0, 0, 1]]).T
    yaxis = np.array([[0, 0, 0, 1],
                      [0, scale, 0, 1]]).T
    zaxis = np.array([[0, 0, 0, 1],
                      [0, 0, scale, 1]]).T

    xc = A.dot(xaxis)
    yc = A.dot(yaxis)
    zc = A.dot(zaxis)

    if draw_2d:
        ax.plot(xc[0, :], xc[1, :], 'r' + style)
        ax.plot(yc[0, :], yc[1, :], 'g' + style)
    else:
        ax.plot(xc[0, :], xc[1, :], xc[2, :], 'r' + style)
        ax.plot(yc[0, :], yc[1, :], yc[2, :], 'g' + style)
        ax.plot(zc[0, :], zc[1, :], zc[2, :], 'b' + style)


def rotateZ(theta):
    rz = np.array([[math.cos(theta), - math.sin(theta), 0, 0],
                   [math.sin(theta), math.cos(theta), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    return rz


def translate(dx, dy, dz):
    t = np.array([[1, 0, 0, dx],
                  [0, 1, 0, dy],
                  [0, 0, 1, dz],
                  [0, 0, 0, 1]])
    return t


def FK(angle, link):
    n_links = len(link)
    P = []
    P.append(np.eye(4))
    for i in range(0, n_links):
        R = rotateZ(angle[i] / 180 * math.pi)
        T = translate(link[i], 0, 0)
        P.append(P[-1].dot(R).dot(T))
    return P


def IK(target, angle, link, max_iter=10000, err_min=0.1):
    solved = False
    err_end_to_target = math.inf

    for loop in range(max_iter):
        for i in range(len(link) - 1, -1, -1):
            P = FK(angle, link)
            end_to_target = target - P[-1][:3, 3]
            err_end_to_target = math.sqrt(end_to_target[0] ** 2 + end_to_target[1] ** 2)
            if err_end_to_target < err_min:
                solved = True
            else:
                cur_to_end = P[-1][:3, 3] - P[i][:3, 3]
                cur_to_end_mag = math.sqrt(cur_to_end[0] ** 2 + cur_to_end[1] ** 2)
                cur_to_target = target - P[i][:3, 3]
                cur_to_target_mag = math.sqrt(cur_to_target[0] ** 2 + cur_to_target[1] ** 2)

                end_target_mag = cur_to_end_mag * cur_to_target_mag

                if end_target_mag <= 0.0001:
                    cos_rot_ang = 1
                    sin_rot_ang = 0
                else:
                    cos_rot_ang = (cur_to_end[0] * cur_to_target[0] + cur_to_end[1] * cur_to_target[1]) / end_target_mag
                    sin_rot_ang = (cur_to_end[0] * cur_to_target[1] - cur_to_end[1] * cur_to_target[0]) / end_target_mag

                rot_ang = math.acos(max(-1, min(1, cos_rot_ang)))

                if sin_rot_ang < 0.0:
                    rot_ang = -rot_ang

                # Update current joint angle values
                angle[i] = angle[i] + (rot_ang * 180 / math.pi)

                if angle[i] >= 360:
                    angle[i] = angle[i] - 360
                if angle[i] < 0:
                    angle[i] = 360 + angle[i]

        if solved:
            break

    return angle, err_end_to_target, solved, loop


# Have not implemented
def onclick(event):
    global target, link, angle, ax
    target[0] = event.xdata
    target[1] = event.ydata

    print("Target Position : ", target)
    plt.cla()
    ax.set_xlim(-50, 150)
    ax.set_ylim(-50, 150)

    # Inverse Kinematics
    angle, err, solved, iteration = IK(target, angle, link, max_iter=1000)

    P = FK(angle, link)
    for i in range(len(link)):
        start_point = P[i]
        end_point = P[i + 1]
        ax.plot([start_point[0, 3], end_point[0, 3]], [start_point[1, 3], end_point[1, 3]], linewidth=5)
        # draw_axis(ax, scale=5, A=P[i+1], draw_2d=True)

    if solved:
        print("\nIK solved\n")
        print("Iteration :", iteration)
        print("Angle :", angle)
        telnet = telnetlib.Telnet('192.168.1.159')

        if round(angle[0]) < 160 and round(angle[1]) < 160:
            d_angle = (90-(360 - round(angle[0]) - round(angle[1]) - 90))
            if d_angle < 0:
                d_angle = 0
            s = f'A{0} B{round(angle[0])} C{180 - round(angle[1])} D{d_angle} \n'
            s_new = f'A{0} B{round(angle[0]) + random.randint(1, 3)} C{180-round(angle[1]) + random.randint(1, 3)} D90\n'

            print(s_new)

            telnet.write(s.encode())
            time.sleep(0.05)
            telnet.write(s_new.encode())
            time.sleep(0.05)

        else:
            print('IK ERROR')
        print("Target :", target)
        print("End Effector :", P[-1][:3, 3])
        print("Error :", err)
    else:
        print("\nIK error\n")
        print("Angle :", angle)
        print("Target :", target)
        print("End Effector :", P[-1][:3, 3])
        print("Error :", err)
    fig.canvas.draw()

def go_to(targets,an,rotate):
    global target, link, angle, ax
    target[0] = targets[0]
    target[1] = targets[1]

    print("Target Position : ", target)
    plt.cla()
    ax.set_xlim(-50, 150)
    ax.set_ylim(-50, 150)

    # Inverse Kinematics
    angle, err, solved, iteration = IK(target, angle, link, max_iter=1000)

    P = FK(angle, link)
    for i in range(len(link)):
        start_point = P[i]
        end_point = P[i + 1]
        ax.plot([start_point[0, 3], end_point[0, 3]], [start_point[1, 3], end_point[1, 3]], linewidth=5)
        # draw_axis(ax, scale=5, A=P[i+1], draw_2d=True)

    if solved:
        #print("\nIK solved\n")
        #print("Iteration :", iteration)
        #print("Angle :", angle)
        telnet = telnetlib.Telnet('192.168.1.159')
        if round(angle[0]) < 300 and round(angle[1]) < 300:
            s = f'S150 A{an} B{round(angle[0])} C{round(angle[1])}  D90\n'
            s_new = f'S150 A{180-an} B{round(angle[0]) + random.randint(1, 3)} C{180-round(angle[1]) + random.randint(1, 3)} Z150\n'

            #print(s)

            telnet.write(s_new.encode())
            time.sleep(0.05)
            return s

        else:
            print('IK ERROR')
        #print("Target :", target)
        #print("End Effector :", P[-1][:3, 3])
        #print("Error :", err)
    else:
        print("\nIK error\n")
        #print("Angle :", angle)
        #print("Target :", target)
        #print("End Effector :", P[-1][:3, 3])
        #print("Error :", err)
    fig.canvas.draw()


def main():
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.suptitle("Cyclic Coordinate Descent - Inverse Kinematics", fontsize=12)
    ax.set_xlim(-50, 150)
    ax.set_ylim(-50, 150)

    # Forward Kinematics
    P = FK(angle, link)
    # Plot Link
    for i in range(len(link)):
        start_point = P[i]
        end_point = P[i + 1]
        ax.plot([start_point[0, 3], end_point[0, 3]], [start_point[1, 3], end_point[1, 3]], linewidth=5)
        # draw_axis(ax, scale=5, A=P[i+1], draw_2d=True)
    plt.show()


if __name__ == "__main__":
    main()