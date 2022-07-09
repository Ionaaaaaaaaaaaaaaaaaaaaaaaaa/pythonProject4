import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
dir = input('Please enter the name of the directory ')
coordTname = input('Please enter the path for coordT ')
Defectsname = input('Please enter the path for defects')
coordT = pd.read_csv(coordTname,header=None)
coordT.drop([0],axis = 0,inplace = True)

defects = np.load(Defectsname,allow_pickle='True').item()
key = input('Please enter the name of the defect ')
Ftime = float(input('Please enter the final step '))
Animationname = input('Please enter the name of the file where to save animation ')
coordT.set_index(0, drop=True, inplace=True)
print(coordT)
X = {}
Y = {}
Z = {}
for j in coordT[1].unique():
    if j>Ftime:
        break
    X.update({'x ' + str(j): []})
    Y.update({'x ' + str(j): []})
    Z.update({'x ' + str(j): []})
    nu = 0
    X['x ' + str(j)].extend([i[1] for i in defects[key] if coordT[1][i[0]] == j])
    Y['x ' + str(j)].extend([i[2] for i in defects[key] if coordT[1][i[0]] == j])
    Z['x ' + str(j)].extend([i[3] for i in defects[key] if coordT[1][i[0]] == j])


print (X)
#print (Y)
#print (Z)
K = [i for i in X.keys()]
print(K)
#fig = plt.figure(figsize = (20,10))
#ax = fig.add_subplot(projection='3d')
#for i in K:
    #sc = ax.scatter(X[i], Y[i], Z[i])
#plt.show()

fig = plt.figure(figsize=(15,6))
ax = p3.Axes3D(fig)
ax.set_box_aspect([1,1,2])
limits = [-0.01,0.01,-0.01,0.01]
ax.axis(limits)
x = [0, 0]
y = [0, 0]
z = [0.01, -0.01]

points, = ax.plot(x, y, z, '.')
def update_points(num, x, y, z, points):
    x = [0, 0, -0.01, 0.01]
    y = [0, 0, 0, 0]
    z = [0.01, -0.01, 0 , 0 ]
    k = [i for i in coordT[1].unique()]
    j = k[num]
    x.extend([i[1] for i in defects[key] if coordT[1][i[0]] <= j])
    y.extend([i[2] for i in defects[key] if coordT[1][i[0]] <= j])
    z.extend([i[3] for i in defects[key] if coordT[1][i[0]] <= j])


    points.set_data(x, y)
    points.set_3d_properties(z, 'z')
    return points
ani = animation.FuncAnimation(fig, update_points, frames=len(coordT[1].unique()), fargs=(x, y, z, points))

ani.save(dir + Animationname + '.gif', writer='Pillow', fps=3)

plt.show()
