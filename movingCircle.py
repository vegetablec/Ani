import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import ffmpeg

fig, ax= plt.subplots()
r = 1

dx = 1
dy = 10

v = 6#圆心在xy坐标上一秒移动的快慢
f = 20 #转圈的快慢，数字越大越快
n = 200 # n*200=图像一共的帧数,n为一共转的圈数
#图像一共nf秒
m = 20 #一圈的点数,应为偶数
a=1 #数据保留1为保留全部数据，2为保留最后50条，3为不保留数据

#--------------------------------------------------

#
x0 = -8*r
y0 = dy/2
sx = 0
sy = 0
detx = 0 
dety = -1
#

start = time.perf_counter()

def getXY(t):
    x = np.cos(t)
    y = np.sin(t)
    return x, y

def getX0Y0(frame):
    t = int(frame*250/np.pi)
    dv = v/100
    global detx,dety,sx,sy,x0,y0
    if dety==-1 and detx==0:
        y0 = y0-dv
        sy = sy+dv
        if int(sy) == dy:
            detx = 1
            dety = 0
            sy=0
    elif dety==1 and detx==0:
        y0 = y0+dv
        sy = sy+dv
        if int(sy)==dy:
            detx = 1
            dety = 0
            sy=0
    elif dety==0 and detx==1:
        x0 = x0+dv
        sx = sx+dv
        if int(sx)==dx and int(y0)==dy/2:
            dety = -1
            detx = 0
            sx = 0
        elif int(sx)==dx and int(y0)==(-dy/2):
            dety = 1
            detx = 0
            sx = 0
    return x0,y0
    

xs, ys = [],[]
for i in range(0,50):
    xs.append(0)
    ys.append(0)

circle_ani, = ax.plot([], [], 'r', markersize=0.5)

def init():
    ax.set_xlim(-10*r, 10*r)
    ax.set_ylim(-10*r, 10*r)
    del xs[:]
    del ys[:]
    circle_ani.set_data(xs,ys)

    return circle_ani,

def updata(frame):
    t = int(frame*m/2/np.pi)
    frame = frame%(2*np.pi)
    # if t==100:
    #     end = time.perf_counter()
    #     print(end-start)
    x, y = getXY(frame)
    x0, y0 = getX0Y0(frame)
    x = x0 + r*x
    y = y0 + r*y
    xs.append(x)
    ys.append(y)
    #print(t,x0,y0)
    if a==1:
        circle_ani.set_data(xs, ys)
        return circle_ani,
    elif a==2:
        circle_ani.set_data(xs[t-50:t], ys[t-50:t])
        return circle_ani,
    elif a==3:
        circle_ani.set_data(x, y)
        return circle_ani,
    

ani = FuncAnimation(fig, updata, np.linspace(0,n*2*np.pi,n*m), interval=(10/f), init_func=init, blit=True, repeat=False)
#ani.save('ani.gif', writer='pillow',fps=10)
plt.show()
