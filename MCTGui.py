import tkinter as tk
from tkinter import *
import tkinter.messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# r = 1 #圆的半径

# dx = 2 #x轴上的距离
# dy = 10 #y轴上的距离

# v = 10#圆心在xy坐标上一秒移动的快慢
# f = 40 #Hz,一秒的圈数
# n = 200 # n为一共转的圈数
# #图像一共n/f秒
# m = 200 #一圈的点数,应为偶数
# #图像一共nm个点

window = tk.Tk()
window.title('Simulater')
window.geometry('800x600')

def get_data():
    global r, dx, dy, v, f, n, m, w
    r = float(r_entry.get())
    dx = float(dx_entry.get())
    dy = float(dy_entry.get())
    v = float(v_entry.get())
    f = int(f_entry.get())
    n = int(n_entry.get())
    m = int(m_entry.get())
    w = float(w_entry.get())

def set_data():
    global r, dx, dy, v, f, n, m, w
    r_entry.select_clear()
    r_entry.insert(0, r)
    dx_entry.select_clear()
    dx_entry.insert(0, dx)
    dy_entry.select_clear()
    dy_entry.insert(0, dy)
    v_entry.select_clear()
    v_entry.insert(0, v)
    f_entry.select_clear()
    f_entry.insert(0, f)
    n_entry.select_clear()
    n_entry.insert(0, n)
    m_entry.select_clear()
    m_entry.insert(0, m)
    w_entry.select_clear()
    w_entry.insert(0, w)

def read_file():  
    try:
        with open("MCTconfig", 'r') as F:
            para = F.readline()
    except:
        with open("MCTconfig", "w") as F:
            para='1.5,4.0,10.0,10.0,40,400,200,1.5'
            F.write(para)
    paras = para.split(',')
    #print(paras)
    global r, dx, dy, v, f, n, m, w
    r = float(paras[0])
    dx = float(paras[1])
    dy = float(paras[2])
    v = float(paras[3])
    f = int(paras[4])
    n = int(paras[5])
    m = int(paras[6])
    w = float(paras[7])


def init():
    global x0,y0,sx,sy,detx,dety,r,dy
    x0 = -8*r
    y0 = dy/2
    sx = 0
    sy = 0
    detx = 0 
    dety = -1

def getXY(t):
    t = (t%m)/m*2*np.pi
    x = np.cos(t)
    y = np.sin(t)
    return x, y

def getX0Y0():
    dv = v/f/m
    global detx,dety,sx,sy,x0,y0,dx,dy
    if dety==-1 and detx==0:
        y0 = y0-dv
        sy = sy+dv
        #print(y0, sy)
        if abs(sy-dy) <= 1e-4:
            detx = 1
            dety = 0
            #print("change dir", y0,sy)
            sy=0
    elif dety==1 and detx==0:
        y0 = y0+dv
        sy = sy+dv
        if abs(sy-dy) <= 1e-4:
            detx = 1
            dety = 0
            sy=0
    elif dety==0 and detx==1:
        x0 = x0+dv
        sx = sx+dv
        #print(y0+(dy/2))
        if abs(sx-dx)<=1e-4 and abs(y0-(dy/2))<=1e-4:
            dety = -1
            detx = 0
            sx = 0
        elif abs(sx-dx)<=1e-4 and abs(y0+(dy/2))<=1e-4:
            dety = 1
            detx = 0
            sx = 0
    return x0,y0

def get_img():
    get_data()
    init()
    #print(r,v,dx,dy,f,n,m)
    fig, ax= plt.subplots()
    l = 'r=' + str(r) + '  dx=' + str(dx) + '  dy=' + str(dy) + '  v=' + str(v) + '  f=' + str(f)
    plt.xlabel(l)
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
    lc = LineCollection(segment, colors=color, linewidth = w)
    ax.add_collection(lc)
    ax.set_xlim(-10*r, 10*r)
    ax.set_ylim(-10*r, 10*r)
    ax.set_aspect(1)
    ax.autoscale()
    plt.show()

def save_donfig():
    global r,dx,dy,v,f,n,m,w
    get_data()
    conf = str(r)+','+str(dx)+','+str(dy)+','+str(v)+','+str(f)+','+str(n)+','+str(m)+','+str(w)
    #print(conf)
    with open("config", "w") as F:
        F.write(conf)
    tkinter.messagebox.showinfo(title = "save successful", message='保存成功')
    


r_lable = tk.Label(window, text='半径')
r_lable.pack()
r_entry = tk.Entry(window,show = None)
r_entry.pack()

v_lable = tk.Label(window, text='速度')
v_lable.pack()
v_entry = tk.Entry(window,show = None)
v_entry.pack()

dx_lable = tk.Label(window, text='x轴距离')
dx_lable.pack()
dx_entry = tk.Entry(window,show = None)
dx_entry.pack()

dy_lable = tk.Label(window, text='y轴距离')
dy_lable.pack()
dy_entry = tk.Entry(window,show = None)
dy_entry.pack()

f_lable = tk.Label(window, text='频率')
f_lable.pack()
f_entry = tk.Entry(window,show = None)
f_entry.pack()

n_lable = tk.Label(window, text='一共转的圈数')
n_lable.pack()
n_entry = tk.Entry(window,show = None)
n_entry.pack()

m_lable = tk.Label(window, text='一圈的点数，越大越像圆')
m_lable.pack()
m_entry = tk.Entry(window,show = None)
m_entry.pack()
w_lable = tk.Label(window, text='线条粗细')
w_lable.pack()
w_entry = tk.Entry(window, show=None)
w_entry.pack()

b_getimg = tk.Button(window, text='生成图像', command=get_img)
b_getimg.pack()

b_savecof = tk.Button(window, text="保存现有参数", command=save_donfig)
b_savecof.pack()





if __name__ == "__main__":
    read_file()
    set_data()
    window.mainloop()
