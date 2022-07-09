import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
coordT.set_index(0, drop=True, inplace=True)
print(coordT)
X = {}
Y = {}
Z = {}
for j in coordT[1].unique():
    if j>Ftime:
        break
    X.update({'x ' + str(j): [i[1] for i in defects[key] if coordT[1][i[0]] == j]})
    Y.update({'x ' + str(j): [i[2] for i in defects[key] if coordT[1][i[0]] == j]})
    Z.update({'x ' + str(j): [i[3] for i in defects[key] if coordT[1][i[0]] == j]})
Xdf = pd.DataFrame.from_dict(X,orient='index').T
Ydf = pd.DataFrame.from_dict(Y,orient='index').T
Zdf = pd.DataFrame.from_dict(Z,orient='index').T


Xdf.to_csv(dir + 'Xdf.csv')
Ydf.to_csv(dir + 'Ydf.csv')
Zdf.to_csv(dir + 'Zdf.csv')
