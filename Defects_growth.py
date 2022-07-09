import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
dir = input('Please enter the name of the directory ')
coordTname = input('Please enter the path for coordT ')
Defectsname = input('Please enter the path for defects')
coordT = pd.read_csv(coordTname,header=None)
coordT.drop([0],axis = 0,inplace = True)
Ftime = float(input('Please enter the final step '))
defects = np.load(Defectsname,allow_pickle='True').item()

coordT.set_index(0, drop=True, inplace=True)
print(coordT)
X = {}
Y = {}
Z = {}
print(coordT[1][156399.0])
for j in defects.keys():

    X.update({'x ' + j:[]})
    Y.update({'x ' + j: []})
    Z.update({'x ' + j: []})
    nu = 0
    X['x ' + j].extend([i[1] for i in defects[j] if coordT[1][i[0]] <= Ftime])
    Y['x ' + j].extend([i[2] for i in defects[j] if coordT[1][i[0]] <= Ftime])
    Z['x ' + j].extend([i[3] for i in defects[j] if coordT[1][i[0]] <= Ftime])


print (X)
#print (Y)
#print (Z)
K = [i for i in X.keys()]
fig = plt.figure(figsize = (20,10))
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1,1,2])
for i in K:
    sc = ax.scatter(X[i], Y[i], Z[i],s=2)
plt.show()