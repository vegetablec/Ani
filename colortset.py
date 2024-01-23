import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# lines = np.array([
#     [[0, 0], [1, 1]],  # 第一条线段
#     [[1, 0], [0, 1]]   # 第二条线段
# ])
# color = [(0/255,255/255,255/255), (0/255, 0/255, 255/255)]
x = np.linspace(0, 5, 600)
y = np.linspace(0, 5, 600)
ps = np.stack((x,y), axis=1)
segment = np.stack((ps[:-1], ps[1:]), axis=1)
color = []
num1 = np.linspace(1,0,300)
num2 = np.linspace(0,1,300)
for i in num1:
    color.append((i, 0, 0))
for i in num2:
    color.append((0, 0, i))
lc = LineCollection(segment, colors=color)
fig, ax = plt.subplots()
ax.add_collection(lc)
fig.set_xlim(0, 1)
fig.set_ylim(0, 1)
ax.autoscale()
plt.show()