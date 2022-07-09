import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
Choice1 = input('Would tou like to use an already existing file with broken bonds or create a new one? Print exist/new respectivly ')
Choice1.lower()
if Choice1 == 'new':
    dir = input('Please enter the name of the directory ')
    bondsname = input('Please enter the filename for bonds ')
    partname = input('Please enter the filename for particles ')
    partnamedf = input('Please enter the name of the file where to save partdf ')
    bondnamedf = input('Please enter the name of the file where to save bonddf ')
    coordT = input('Please enter the name of the file where to save info about broken bonds ')
    data = pd.read_csv(dir + bondsname + ".txt", sep=' ', header=None)
    datapart = pd.read_csv(dir + partname + ".txt", sep=' ', header=None)
    data = data.drop([0, 2, 5, 6], axis='columns')
    data.set_index(data[1], drop=True, inplace=True)
    datapart.set_index(datapart[1], drop=True, inplace=True)
    datapart = datapart.drop([0, 1], axis='columns')
    print(data)
    print(datapart)


    def get_dataInd_and_Col(data):

        I = [i for i in data.index]
        C = [i for i in data.columns]
        return I, C


    def parsingPart(datapart):
        p = {}
        for j in datapart.index:
            t = {}
            for i in datapart.columns:
                if datapart[i][j] == 2:
                    t.update(
                        {datapart[i + 1][j]: np.array([datapart[i + 3][j], datapart[i + 4][j], datapart[i + 5][j]])})
            p.update({j: t})
        df = pd.DataFrame(p).T
        print(df)
        df.to_csv(dir + partnamedf + ".csv")
        return df


    def coordInfodf(data, datadf):
        b = {}
        for i in data.index:
            t = {}
            for j in datadf.columns:
                t.update({j: np.array([(datadf[j][data[3][i]][0] + datadf[j][data[4][i]][0]) / 2,
                                       (datadf[j][data[3][i]][1] + datadf[j][data[4][i]][1]) / 2,
                                       (datadf[j][data[3][i]][2] + datadf[j][data[4][i]][2]) / 2])})
            b.update({i: t})
        df = pd.DataFrame(b).T
        print(df)
        df.to_csv(dir + bondnamedf + ".csv")
        return df


    def brokenbondstimes(data, bonddf):
        b = {}
        used = np.array([])
        I, C = get_dataInd_and_Col(data)
        for i in range(0, len(I)):
            for j in range(0, len(C)):
                if data[C[j - 1]][I[i]] not in used:
                    if data[C[j]][I[i]] == 18 and data[C[j + 1]][I[i]] == 0 and I[i] not in used and data[C[j - 1]][
                        I[i]] != 0:
                        b.update({data[C[j - 1]][I[i]]: np.array([I[i]])})
                        used = np.append(used, data[C[j - 1]][I[i]])
                        used = np.append(used, I[i])
                else:
                    if data[C[j]][I[i]] == 18 and data[C[j + 1]][I[i]] == 0 and I[i] not in used and data[C[j - 1]][
                        I[i]] != 0:
                        b[data[C[j - 1]][I[i]]] = np.append(b[data[C[j - 1]][I[i]]], I[i])
                        used = np.append(used, I[i])
        co = {}
        bk = [i for i in b.keys()]
        bk = sorted(bk)
        print(bk)
        for i in bk:
            for j in b[i]:
                co.update({j: [i, bonddf[i][j][0], bonddf[i][j][1], bonddf[i][j][2]]})

        df = pd.DataFrame(co).T
        print(df)
        df.to_csv(dir + coordT + ".csv")
        # np.save("D:/MUSEN Materials/Musen export/dictopt.npy", b)
        # np.savetxt("D:/MUSEN Materials/Musen export/dictopt.txt", b)
        return b, df


    partdf = parsingPart(datapart)
    bonddf = coordInfodf(data, partdf)
    b,TBonddf = brokenbondstimes(data, bonddf)


Choice = input('Please enter the type of analysis, you would like to perform: if you want to finish enter stop, if you want to get defects on one step print 1 if you want to get defects on muliple steps print 2 ')
Choice.lower()

if Choice == 'stop':
    print('end')
elif Choice == '1':
    dir = input('Please enter the name of the directory ')
    defectsName = input('Please enter the name of the file where to save the defects ')
    defSizename = input('Please enter the name of the file where to save the sizes of the defects ')
    if Choice1 == 'exist':
        coordTname = input('Please enter the path for the file that contains info about broken bonds ')
        coordT = pd.read_csv(coordTname, header=None)
        coordT.drop([0], axis=0, inplace=True)
        coordT.set_index(0, drop=False, inplace=True)
    elif Choice1 == 'new':
        coordT = TBonddf

    # print(coordT)
    Ftime = float(input('Please enter the final step '))
    r = float(input('Please enter the max distance '))


    def Get_defects(coordT, Ftime, r):
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
        return defects
    defects = Get_defects(coordT, Ftime, r)

    np.save(dir + defectsName + str(Ftime) + '.npy', defects)
    defectsdf = pd.DataFrame.from_dict(defects, orient='index')
    defectsdf.to_csv(dir + defectsName + str(Ftime) + '.csv')
    print('end')
    X = {}
    Y = {}
    Z = {}
    for j in defects.keys():
        # print(defects[j])
        X.update({'x ' + j: []})
        Y.update({'x ' + j: []})
        Z.update({'x ' + j: []})
        nu = 0
        X['x ' + j].extend([i[1] for i in defects[j]])
        Y['x ' + j].extend([i[2] for i in defects[j]])
        Z['x ' + j].extend([i[3] for i in defects[j]])
    # print (X)
    # print (Y)
    # print (Z)
    K = [i for i in X.keys()]
    fig = plt.figure(figsize=(10, 20))
    ax = fig.add_subplot(projection='3d')
    ax.set_box_aspect([1, 1, 2])
    for i in K:
        sc = ax.scatter(X[i], Y[i], Z[i], s=r * 10000)
    plt.show()
elif Choice == '2':
    dir = input('Please enter the name of the directory ')
    defectsName = input('Please enter the name of the file where to save the defects ')
    defSizename = input('Please enter the name of the file where to save the sizes of the defects ')
    if Choice1 == 'exist':
        coordTname = input('Please enter the path for the file that contains info about broken bonds ')
        coordT = pd.read_csv(coordTname, header=None)
        coordT.drop([0], axis=0, inplace=True)
        coordT.set_index(0, drop=False, inplace=True)
    elif Choice1 == 'new':
        coordT = TBonddf
    #coordT.drop([0], axis=0, inplace=True)
    #coordT.set_index(0, drop=False, inplace=True)
    # print(coordT)
    Ftime = float(input('Please enter the final step '))
    r = float(input('Please enter the max distance '))
    step = int(input('Please enter the saving step '))


    def Get_defects(coordT, Ftime, r, step, defSizename, defectsName):
        coordT = coordT[coordT[1] <= Ftime]
        Timelist = [i for i in coordT[1].unique()]
        for j in range(0, len(Timelist), step):
            time = Timelist[j]
            coordTi = coordT[coordT[1] <= time]
            # print(coordTi.index)
            # coordTi.drop([0], axis=1, inplace=True)
            defects = {'defect_0': [
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
            np.save(dir + defectsName + '_' + str(Ftime) + '_' + str(time) + '.npy', defects)
            defectsdf = pd.DataFrame.from_dict(defects, orient='index')
            defectsdf.to_csv(dir + defectsName + '_' + str(Ftime) + '_' + str(time) + '.csv')
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
            defsdf = pd.DataFrame(Defsize).T
            defsdf.to_csv(dir + defSizename + str(Ftime) + str(time) + '.csv')
            print('step_', time)
        return defects
    defects = Get_defects(coordT, Ftime, r, step, defSizename, defectsName)
    print('end')
    end = input('Enter any letter ')