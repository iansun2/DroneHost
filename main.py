import threading
import time
import csv
import numpy as np
import math as m
import rotate as r
import matplotlib.pyplot as plt
import matplotlib.animation as ani_plt
import controller as ctrl
import connection as conn

thread_pool = []

def debug():
    while True:
        time.sleep(0.1)
        #print(target_attitude_str)
        #print(current_drone_pack)
        #print(rx_buffer_len)
        #print(frame)
        #print(qw_str)
        #print(qx_str)
        #print(qy_str)
        #print(qz_str)
        #print("=\n=\n=\n=\n")
        #print(rx_buffer)
        #print("=\n=\n=\n=\n")
        


debug_thread = threading.Thread(target= debug)
debug_thread.start()


controller = ctrl.Controller()


drone_connection = conn.DroneConnection("172.16.0.171", 9000, controller, thread_pool)
#drone_connection = conn.DroneConnection("127.0.0.1", 9000, controller, thread_pool)

app_connection = conn.AppConnection("0.0.0.0", 9001, controller, thread_pool)





def upd_view(frame):
    q = controller.current_attitude.get()
    #q = np.array([1, 0, 0, 0])
    vx = r.qv_mult(q , np.array([1,0,0]))
    vy = r.qv_mult(q , np.array([0,1,0]))
    vz = r.qv_mult(q , np.array([0,0,1]))

    VIEW_SIZE = 100
    VECT_SCALE = 30
    viewX = np.array([VIEW_SIZE, 0, 0])
    viewY = np.array([0, VIEW_SIZE, 0])
    viewZ = np.array([0, 0, VIEW_SIZE])

    ax.cla()
    ax.set_xlim([-VIEW_SIZE, VIEW_SIZE])
    ax.set_ylim([-VIEW_SIZE, VIEW_SIZE])
    ax.set_zlim([-VIEW_SIZE, VIEW_SIZE])
    #ax.scatter(pos[0], pos[1], pos[2])
    ax.quiver(0, 0, 0, viewX[0], viewX[1], viewX[2], color=(255/255, 200/255, 200/255))
    ax.quiver(0, 0, 0, viewY[0], viewY[1], viewY[2], color=(200/255, 255/255, 200/255))
    ax.quiver(0, 0, 0, viewZ[0], viewZ[1], viewZ[2], color=(200/255, 200/255, 255/255))
    ax.quiver(0, 0, 0, vx[0]*VECT_SCALE, vx[1]*VECT_SCALE, vx[2]*VECT_SCALE, color=(255/255, 0/255, 0/255))
    ax.quiver(0, 0, 0, vy[0]*VECT_SCALE, vy[1]*VECT_SCALE, vy[2]*VECT_SCALE, color=(0/255, 255/255, 0/255))
    ax.quiver(0, 0, 0, vz[0]*VECT_SCALE, vz[1]*VECT_SCALE, vz[2]*VECT_SCALE, color=(0/255, 0/255, 255/255))



fig = plt.figure()
ax = fig.add_subplot(projection='3d')
#ani = ani_plt.FuncAnimation(fig, upd_view, interval=50)

#plt.show()

for thread in thread_pool:
    thread.start()


for thread in thread_pool:
    thread.join()

while True:
    a = 0