import numpy as np
import pandas as pd


dir = input('Please enter the name of the directory ')
coordTname = input('Please enter the path for the file that contains info about broken bonds ')
defectsName = input('Please enter the name of the file where to save the defects ')
#defSizename = input('Please enter the name of the file where to save the sizes of the defects ')
defSizename = input('Please enter the name of the file where to save the sizes of the defects ')
coordT = pd.read_csv(coordTname,header=None)
coordT.drop([0],axis = 0,inplace = True)
coordT.set_index(0,drop=False,inplace=True)
#print(coordT)
Ftime = float(input('Please enter the final step '))
r = float(input('Please enter the max distance '))
step = int(input('Please enter the saving step '))

def Get_defects(coordT,Ftime,r,step,defSizename,defectsName):
    coordT = coordT[coordT[1] <= Ftime]
    Timelist = [i for i in coordT[1].unique()]
    for j in range (0,len(Timelist),step):
        time = Timelist[j]
        coordTi = coordT[coordT[1] <= time]
        #print(coordTi.index)
        # coordTi.drop([0], axis=1, inplace=True)
        defects = {'defect_0': [
            [coordTi[0][coordTi.index[0]], coordTi[2][coordTi.index[0]], coordTi[3][coordTi.index[0]],
             coordTi[4][coordTi.index[0]]]]}
        ind = 0
        param = True
        used = []
        flag = 0
        #print(coordTi)
        while param == True:
            keys = [i for i in defects.keys()]
            # print(keys)
            # print(ind)
            key = keys[ind]
            param2 = True
            ind2 = 0
            while param2 == True:
                bn = defects[key][ind2][0]
                # print (bn)
                used.append(bn)
                coordTid = coordTi[(np.sqrt((coordTi[2] - coordTi[2][bn]) ** 2 + (coordTi[3] - coordTi[3][bn]) ** 2 + (
                            coordTi[4] - coordTi[4][bn]) ** 2) < r) & (~coordTi[0].isin(used))]
                # print(coordTid)
                if ((ind2) >= len(defects[key]) - 1) and (len(coordTid.index) == 0):
                    # print('1')
                    ind += 1
                    coordtLeft = coordTi[~coordTi.index.isin(used)]
                    if len(coordtLeft.index) == 0:
                        flag = 1
                        break
                    defects.update({'defect_' + str(ind): [
                        [coordtLeft[0][coordtLeft.index[0]], coordtLeft[2][coordtLeft.index[0]],
                         coordtLeft[3][coordtLeft.index[0]], coordtLeft[4][coordtLeft.index[0]]]]})
                    #print('defect_' + str(ind))
                    break
                elif len(coordTid.index) == 0:
                    ind2 += 1
                    continue
                defects[key].extend(
                    [[coordTid[0][i], coordTid[2][i], coordTid[3][i], coordTid[4][i]] for i in coordTid.index])
                used.extend([i for i in coordTid[0]])
                ind2 += 1
            if flag == 1:
                break
        np.save(dir + defectsName+ '_' + str(Ftime) + '_' +  str (time) + '.npy', defects)
        defectsdf = pd.DataFrame.from_dict(defects, orient='index')
        defectsdf.to_csv(dir + defectsName+ '_' + str(Ftime) + '_' +  str (time) + '.csv')
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
                    num += 1
            Centerx = Centerx / num
            Centery = Centery / num
            Centerz = Centerz / num

            Rad.update({i: [Centerx, Centery, Centerz]})
        # print (Rad)
        Defsize = {}
        for i in Rad.keys():
            Defsize.update({i: [len(defects[i]), Rad[i][0], Rad[i][1], Rad[i][2]]})
        #print(Defsize)
        # np.save("D:/MUSEN Materials/Musen export/" + defSizename + ".npy",Defsize)
        defsdf = pd.DataFrame(Defsize).T
        defsdf.to_csv(dir + defSizename + str (Ftime) + str(time) + '.csv')
        print('step_',time)
    return defects
defects = Get_defects(coordT,Ftime,r,step,defSizename,defectsName)
print('end')

