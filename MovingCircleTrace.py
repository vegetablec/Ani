import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
import time
import ffmpeg

fig, ax= plt.subplots()

r = 1 #圆的半径

dx = 2 #x轴上的距离
dy = 10 #y轴上的距离

v = 10#圆心在xy坐标上一秒移动的快慢
f = 40 #Hz,一秒的圈数
n = 200 # n为一共转的圈数
#图像一共n/f秒
m = 200 #一圈的点数,应为偶数
#图像一共nm个点

#--------------------------------------------------

#
x0 = -8*r
y0 = dy/2
sx = 0
sy = 0
detx = 0 
dety = -1
#

def getXY(t):
    t = (t%m)/m*2*np.pi
    x = np.cos(t)
    y = np.sin(t)
    return x, y

def getX0Y0():
    dv = v/f/m
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
    
ax.set_xlim(-10*r, 10*r)
ax.set_ylim(-10*r, 10*r)
xs, ys = [],[]
color = []
p = np.linspace(0, n*m, n*m)
for i in p:
    x, y = getXY(i)
    xo, yo = getX0Y0()
    xs.append(xo+x*r)
    ys.append(yo+y*r)
ps = np.stack((xs,ys), axis=1)
segment = np.stack((ps[:-1], ps[1:]), axis=1)

num1 = np.linspace(n*m/2, 0, int(n*m/2))
num2 = np.linspace(0, n*m/2, int(n*m/2))
for i in num1:
    color.append((i/(n*m/2), 0, 0))
for i in num2:
    color.append((0, 0, i/(n*m/2)))
#print(color)
lc = LineCollection(segment, colors=color)
ax.add_collection(lc)
ax.set_xlim(-10*r, 10*r)
ax.set_ylim(-10*r, 10*r)
ax.set_aspect(1)
ax.autoscale()
plt.show()










