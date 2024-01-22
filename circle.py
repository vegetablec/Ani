import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig, ax= plt.subplots()

x0 = 0
y0 = 0
r = 1

def getXY(t):
    x = np.cos(t)
    y = np.sin(t)
    return x, y

xs, ys = [],[]
circle_ani, = ax.plot([], [], 'ro')

def init():
    ax.set_xlim(-5*r, 5*r)
    ax.set_ylim(-5*r, 5*r)
    del xs[:]
    del ys[:]
    circle_ani.set_data(xs,ys)


    return circle_ani,

def updata(frame):
    x, y = getXY(frame)
    xs.append(x0+r*x)
    ys.append(y0+r*y)
    t = int(frame*250/np.pi)
    print(t,x,y)
    if len(xs)>100&len(xs)<400:
        circle_ani.set_data(xs[t-100:t], ys[t-100:t])
        return circle_ani,
    elif len(xs)<=100:
        circle_ani.set_data(xs[0:t], ys[0:t])
        return circle_ani,
    # circle_ani.set_data(xs, ys)
    # return circle_ani,

ani = FuncAnimation(fig, updata, np.linspace(0,2*np.pi,500), interval=100, init_func=init, blit=True)
plt.show()
