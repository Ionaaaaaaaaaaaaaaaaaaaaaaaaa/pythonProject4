import pandas as pd
import numpy as np


dir = input('Please enter the directory where to save files ') + '\_'
defectsName = input('Please enter the name of the file where to save defects ')
defSizename = input('Please enter the name of the file where to save info (Size, coordinate of the center) about defects ')
#if Choice1 == 'exist':
coordTname = input('Please enter the location of the file with Broke bonds ')
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

Ftime = float(input('Please enter the final step '))
r = float(input('Please enter the max distance '))
step = float(input('Please enter the clastering step '))
step_save = float(input('Please enter the saving step '))
LayerThickness = float(input('Please enter the height of the layer '))
Layerstep = float(input('Please enter the step for the layers '))
Bord1 = int(input('Please enter the lower limit for the counts '))
Bord2 = int(input('Please enter the upper limit for the counts '))

lower_border = -10
Higher_border = lower_border + LayerThickness
while Higher_border <= 10:
    coordTL = coordT[(coordT[4] <= Higher_border)&(coordT[4] >= lower_border)]
    print(coordTL)
    print('Layer------------------------>',lower_border)
    def Get_defects_loop(coordTL, Ftime, r, defSizename, defectsName, step, step_save):
            coordTL = coordTL[coordTL[1] <= Ftime]
            time = 0
            time1 = 0

            while time <= Ftime:
                time1 += step_save
                # print(time1)
                defdict = {}
                defdict_2 = {}
                while time <= Ftime:
                    time += step
                    # print(time1 + step_save,'   ',time)
                    coordTi = coordTL[(coordTL[1] <= time) & (coordTL[1] >= time - step)]
                    if len(coordTi.index) == 0:
                        # print ('1')
                        time += step
                        continue

                    # print(coordTi.index)
                    # coordTi.drop([0], axis=1, inplace=True)
                    defects = {'defect_0_' + str(time): [
                        [coordTi[0][coordTi.index[0]], coordTi[2][coordTi.index[0]], coordTi[3][coordTi.index[0]],
                         coordTi[4][coordTi.index[0]]]]}
                    ind = 0
                    param = True
                    used = []
                    flag = 0
                    # print(coordTi)
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
                            coordTid = coordTi[
                                (np.sqrt((coordTi[2] - coordTi[2][bn]) ** 2 + (coordTi[3] - coordTi[3][bn]) ** 2 + (
                                        coordTi[4] - coordTi[4][bn]) ** 2) < r) & (~coordTi[0].isin(used))]
                            # print(coordTid)
                            if ((ind2) >= len(defects[key]) - 1) and (len(coordTid.index) == 0):
                                # print('1')
                                ind += 1
                                coordtLeft = coordTi[~coordTi.index.isin(used)]
                                if len(coordtLeft.index) == 0:
                                    flag = 1
                                    break
                                defects.update({'defect_' + str(ind) + '_' + str(time): [
                                    [coordtLeft[0][coordtLeft.index[0]], coordtLeft[2][coordtLeft.index[0]],
                                     coordtLeft[3][coordtLeft.index[0]], coordtLeft[4][coordtLeft.index[0]]]]})
                                # print('defect_' + str(ind))
                                break
                            elif len(coordTid.index) == 0:
                                ind2 += 1
                                continue
                            defects[key].extend(
                                [[coordTid[0][i], coordTid[2][i], coordTid[3][i], coordTid[4][i]] for i in
                                 coordTid.index])
                            used.extend([i for i in coordTid[0]])
                            ind2 += 1
                        if flag == 1:
                            break
                    # np.save(dir + defectsName + '_' + str(Ftime) + '_' + str(time) + '.npy', defects)

                    defectsdf = pd.DataFrame.from_dict(defects, orient='index')
                    defdict_2.update({time: defectsdf})
                    # defectsdf.to_csv(dir + defectsName + '_' + str(Ftime) + '_' + str(time) + '.csv')
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
                    # print(Defsize)
                    # np.save("D:/MUSEN Materials/Musen export/" + defSizename + ".npy",Defsize)
                    defsdf = pd.DataFrame.from_dict(Defsize, orient='index', columns=['Size', 'X', 'Y', 'Z'])
                    # print (defsdf)

                    defdict.update({time: defsdf})
                    if round(time, 9) >= (round(time1, 9) + step_save):
                        print(defdict.keys())
                        if len(defdict.keys()) >= 1:
                            # print (defdict.keys())
                            keys = np.array([i for i in defdict.keys()])
                            keys_2 = np.array([i for i in defdict_2.keys()])
                            m = pd.concat([defdict[keys[i]] for i in range(len(keys))])
                            n = pd.concat([defdict_2[keys_2[i]] for i in range(len(keys_2))])
                            m.to_csv(dir + defSizename + '_' + str(Ftime) + '_' + str(time1) + '.csv')
                            n.to_csv(dir + defectsName + '_' + str(Ftime) + '_' + str(time1) + '.csv')
                        break
                    # print('step_', time)
                continue



    defects = Get_defects_loop(coordT, Ftime, r, defSizename, defectsName, step, step_save)
    lower_border += Layerstep
    Higher_border = lower_border + LayerThickness

print('end')
end = input('Enter any letter ')
