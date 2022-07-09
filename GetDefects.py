import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import mpl_toolkits.mplot3d.axes3d as p3
#from matplotlib import animation
#bonddfname = input('Please enter the filename for bondsdf ')
dir = input('Please enter the name of the directory ')
coordTname = input('Please enter the path for the file that contains info about broken bonds ')
st = int(input('Please enter the amount of steps when the growth of the defects stops '))
#figname = input('Please enter the filename for plot ')
#Animationname = input('Please enter the name of the file where to save animation ')
defectsName = input('Please enter the name of the file where to save the defects ')
defSizename = input('Please enter the name of the file where to save the sizes of the defects ')
#bonddf = pd.read_csv("D:/MUSEN Materials/Musen export/" + bonddfname +".csv",header=None)
coordT = pd.read_csv(coordTname,header=None)
coordT.drop([0],axis = 0,inplace = True)
print(coordT)
Ftime = float(input('Please enter the final step '))
r = float(input('Please enter the max distance '))
coordTFtime = coordT[coordT[1] <= Ftime]
def nearest(coordT,r):
    #r = float(input('Plase enter r '))exttimecoordTdf
    cl = {}
    for i in coordT.index:
        N = coordT[(np.sqrt((coordT[2] - coordT[2][i])**2 + (coordT[3] - coordT[3][i])**2 + (coordT[4] - coordT[4][i])**2) < r) & (coordT.index != i)]
        #print([j for j in N[0]])
        cl.update({coordT[0][i]:[j for j in N[0]]})
    #np.save("D:/MUSEN Materials/Musen export/Closest.npy", cl)
    #print(cl)
    cldf = pd.DataFrame(cl)
    return cldf


def get_defects(coordT,cl,Ftime):
    print(coordT[[1,0]])
    defects = {'defects_1':[[coordT[0][1],coordT[2][1],coordT[3][1],coordT[4][1]]]}
    coordTSt = coordT[coordT[1] <= Ftime]
    used = [coordT[0][1]]
    usedkeys = []
    stop = {}
    indT = 0
    timestop = {}
    timestart = {'defects_1':0.0}
    for i in coordTSt[1].unique():
        ind = 0
        coordTi = coordTSt[coordTSt[1] == i]
        param = False
        print(i)
        while param == False:
            K = [i  if i not in usedkeys else None for i in defects.keys()]
            if ind >= len(K):
                break
            key = K[ind]
            if key == None:
                ind += 1
                continue
            #try:
                 #print(ind, len(defects[K[ind - 1]]))
            #except Exception:
                #pass
            param2 = False
            ind2 = 0
            length = 0

            while param2 == False:
                #print(defects[key])
                bonds = [i[0] for i in defects[key]]
                bond = bonds[ind2]
                #print ('Start ',bonds,bond,cl[bond])
                #print(coordTi)
                coordTid = coordTi[(coordTi[0].isin(cl[bond]) & (~coordTi[0].isin(used)))]
                #print ('coordTid ',coordTid)
                defects[key].extend([[coordTid[0][i],coordTid[2][i],coordTid[3][i],coordTid[4][i]] for i in coordTid.index])
                #print([[coordTid[0][i],coordTid[2][i],coordTid[3][i],coordTid[4][i]] for i in coordTid.index])
                used.extend([i for i in coordTid[0]])
                length += len([i for i in coordTid[0]])
                ind2 += 1
                if key not in timestop.keys():
                    timestop.update({key:i})
                if key in timestop.keys():
                    timestop[key] = i
                if ind2 >= len(bonds):
                    ind += 1
                    #print(coordTleft)
                    coordTleft = coordTi[~coordTi[0].isin(used)]
                    #print('coordTleft ',coordTleft)
                    if len(coordTleft.index) == 0:
                        break
                    if length == 0:
                        if key not in stop.keys():
                            stop.update({key:0})
                        else:
                            stop[key] = stop[key] + 1
                    if key in stop.keys():
                        if stop[key] >= st:
                            defects[key + '_' + str(i)] = defects[key]
                            timestart[key + '_' + str(i)] = timestart[key]
                            timestart.pop(key)
                            usedkeys.append(key + '_' + str(i))
                            usedkeys.append(key)
                            defects.pop(key)

                            timestop.update({key + '_' + str(i):i})
                            timestop.pop(key)


                    #if len(coordTleft.index)!=0:
                    #print('index ',coordTleft.index,coordTleft.index[0])
                    #print('append ',[coordTleft[0][coordTleft.index[0]],coordTleft[2][coordTleft.index[0]],coordTleft[3][coordTleft.index[0]],coordTleft[4][coordTleft.index[0]]])
                    defects.update({'defect_' + str(ind) + '_' + str(indT) + '_' + str(i):[[coordTleft[0][coordTleft.index[0]],coordTleft[2][coordTleft.index[0]],coordTleft[3][coordTleft.index[0]],coordTleft[4][coordTleft.index[0]]]]})
                    timestart.update({'defect_' + str(ind) + '_' + str(indT) + '_' + str(i):i})
                    #usedkeys.append('defect_' + str(ind))
                    used.append(coordTleft[0][coordTleft.index[0]])
                    break

            if ind >= len(K):
                break
        indT += 1
    #print(defects
    print(defects.keys(),len(defects.keys()))
    np.save(dir + defectsName + '.npy', defects)
    #defectsdf = pd.DataFrame(defects)
    return defects,usedkeys,timestop,timestart
cl =  nearest(coordTFtime,r)
#print (cl[4420])
defects,usedkeys,timestop,timestart = get_defects(coordT,cl,Ftime,)
print(defects)
print(usedkeys)
X = {}
Y = {}
Z = {}
for j in defects.keys():

    #print(defects[j])
    X.update({'x ' + j:[]})
    Y.update({'x ' + j: []})
    Z.update({'x ' + j: []})
    nu = 0
    X['x ' + j].extend([i[1] if type(i) !=  'dict' else '0' for i in defects[j]])
    Y['x ' + j].extend([i[2] if type(i) !=  'dict' else '0' for i in defects[j]])
    Z['x ' + j].extend([i[3] if type(i) !=  'dict' else '0' for i in defects[j]])


#print (X)
#print (Y)
#print (Z)
K = [i for i in X.keys()]
fig = plt.figure(figsize = (20,10))
ax = fig.add_subplot(projection='3d')
for i in K:
    sc = ax.scatter(X[i], Y[i], Z[i])
#plt.savefig("D:/MUSEN Materials/" + figname + ".jpg")
#plt.show()

#fig = plt.figure(figsize=(15,6))
#ax = p3.Axes3D(fig)
#limits = [-0.01,0.01,-0.01,0.01]
#ax.axis(limits)
#x = [0, 0]
#y = [0, 0]
#z = [0.01, -0.01]

#points, = ax.plot(x, y, z, '.')
#def update_points(num, x, y, z, points):
    #x = [0, 0, -0.01, 0.01]
    #y = [0, 0, 0, 0]
    #z = [0.01, -0.01, 0 , 0 ]
    #Keys = [i for i in defects.keys()]
    #if len(defects[Keys[num]]) > 1:
        #for k in defects[Keys[num]]:
            #x.extend([i[1] for i in defects[j]])
            #y.extend([i[2] for i in defects[j]])
            #z.extend([i[3] for i in defects[j]])


    #points.set_data(x, y)
    #points.set_3d_properties(z, 'z')
    #return points
#ani = animation.FuncAnimation(fig, update_points, frames=len(X.keys()), fargs=(x, y, z, points))

#ani.save('D:/MUSEN Materials/figs/' + Animationname + '.gif', writer='Pillow', fps=3)

#plt.show()

used = []
Rad = {}
for i in defects.keys():
    rad = []
    Centerx = 0
    Centery = 0
    Centerz = 0
    num = 1
    for j in defects[i]:
        if j not in used:
            Centerx += j[1]
            Centery += j[2]
            Centerz += j[3]
            num+=1
    endtime = timestop[i]
    starttime = timestart[i]
    Centerx = Centerx / num
    Centery = Centery / num
    Centerz = Centerz / num

    Rad.update({i:[Centerx,Centery,Centerz,endtime,starttime]})
#print (Rad)
Defsize = {}
for i in Rad.keys():
    Defsize.update({i:[len(defects[i]),Rad[i][0],Rad[i][1],Rad[i][2],Rad[i][3],Rad[i][4],(Rad[i][3] + Rad[i][4])/2]})
print (Defsize)
#np.save("D:/MUSEN Materials/Musen export/" + defSizename + ".npy",Defsize)
defsdf = pd.DataFrame(Defsize).T
defsdf.to_csv(dir + defSizename + '.csv')
plt.show()