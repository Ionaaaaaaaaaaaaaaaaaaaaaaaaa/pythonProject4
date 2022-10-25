import pandas as pd
import numpy as np
import pickle

def funcexp(x, a, b):
        return a * np.exp(-b * x)


def funcpower(x, a, b):
        return a * (x**-b)

def Get_defects(coordT, Ftime, r,defectsName,defSizename,dir):
        coordTi = coordT[coordT[1] <= Ftime]
        print(coordTi.index)
        # coordTi.drop([0], axis=1, inplace=True)
        defects = {'defect_0': [
            [coordTi[0][coordTi.index[0]], coordTi[2][coordTi.index[0]], coordTi[3][coordTi.index[0]],
             coordTi[4][coordTi.index[0]]]]}
        ind = 0
        param = True
        used = []
        flag = 0
        print(coordTi)
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
                    # print('defect_' + str(ind))
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
        for i in defects.keys():
            if len(defects[i]) >= 1000:
                df = pd.DataFrame(defects[i])
                df.to_csv(dir + i + '_' + str(Ftime) + '.csv')
        defectsdf = pd.DataFrame.from_dict(defects, orient='index')
        defectsdf.to_csv(dir + defectsName + str(Ftime) + '.csv')
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
        Defsize = {}
        for i in Rad.keys():
            Defsize.update({i: [len(defects[i]), Rad[i][0], Rad[i][1], Rad[i][2]]})
        defsdf = pd.DataFrame.from_dict(Defsize, orient='index', columns=['Size', 'X', 'Y', 'Z'])
        defsdf.to_csv(dir + defSizename + str(Ftime) + '.csv')
        pickle.dump(defects, open(dir + 'defects.p', 'wb'))
        pickle.dump(defectsdf, open(dir + 'defectsdict.p', 'wb'))
        pickle.dump(defsdf, open(dir + 'defsizedict.p', 'wb'))
        print('end')
        return defects

def start():
    dir = input('Please enter the directory where to save files ') + '\_'
    defectsName = 'defects'
    defSizename = 'defsize'

    coordTname = input('Please enter the location of the file with Broken bonds ')
    coordT = pd.read_csv(coordTname, header=None)
    coordT.drop([0], axis=0, inplace=True)
    coordT.set_index(0, drop=False, inplace=True)

    col1 = np.array([float(i) for i in coordT[5]])
    col2 = np.array([float(i) for i in coordT[2]])
    col3 = np.array([float(i) for i in coordT[3]])
    col4 = np.array([float(i) for i in coordT[4]])
    coordT[1] = col1
    coordT[2] = col2
    coordT[3] = col3
    coordT[4] = col4
    coordT.drop([5], axis=1, inplace=True)
    coordT.sort_values(by=1, ascending=True, inplace=True)

    print(coordT)
    Ftime = float(input('Please enter the final step '))
    r = float(input('Please enter the max distance '))
    Get_defects(coordT, Ftime, r,defectsName,defSizename,dir)
    print('end')
    input('Press any key ')

