import pandas as pd
import numpy as np

dir = input('Please enter the name of the directory ')
coordTname = input('Please enter the path for coordT ')
coordT = pd.read_csv(coordTname,header=None)
coordT.drop([0],axis = 0,inplace = True)
distCsv = input('please enter the name of the file where to save distances ')
r = float(input('Please enter the radius '))
def nearest(coordT,r):
    #r = float(input('Plase enter r '))exttimecoordTdf
    cl = {}
    dist = []
    distmin = []
    for i in coordT.index:
        N = coordT[(np.sqrt((coordT[2] - coordT[2][i])**2 + (coordT[3] - coordT[3][i])**2 + (coordT[4] - coordT[4][i])**2) < r) & (coordT.index != i)]
        for i in N.index:
            Ni = N[N.index != i]
            M = np.sqrt((Ni[2] - N[2][i]) ** 2 + (Ni[3] - N[3][i]) ** 2 + (Ni[4] - N[4][i]) ** 2)
            #print(M)
            dist.append(np.mean(M))
            distmin.append(np.min(M))
    return dist,distmin
dist,distmin = nearest(coordT,r)
dist = np.array(dist)
DistD = {'dist':[np.min(distmin),np.mean(dist)]}
distDf = pd.DataFrame(DistD).T
distDf.to_csv(dir + distCsv + '.csv')
