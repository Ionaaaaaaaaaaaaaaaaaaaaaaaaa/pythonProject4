import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

coordTname = input('Please enter the path for the file that contains info about broken bonds ')
coordT = pd.read_csv(coordTname,header=None)
coordT.drop([0],axis = 0,inplace = True)

r = 25e-05
def nearest(coordT,r):
    #r = float(input('Plase enter r '))exttimecoordTdf
    cl = {}
    for i in coordT.index:
        N = coordT[(np.sqrt((coordT[2] - coordT[2][i])**2 + (coordT[3] - coordT[3][i])**2 + (coordT[4] - coordT[4][i])**2) < r) & (coordT.index != i)]
        #print([j for j in N[0]])
        cl.update({coordT[0][i]:[j for j in N[0]]})
    #np.save("D:/MUSEN Materials/Musen export/Closest.npy", cl)
    #print(cl)

    cldf = pd.DataFrame.from_dict(cl,orient='index').T
    return cldf

cldf = nearest(coordT,r)
cldf.to_csv('D:\MUSEN Materials\Bigmodeldata\cldf.csv')
print(cldf)


