import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
Choice1 = input('Would tou like to use an already existing file with broken bonds or create a new one? Print exist/new respectivly ')
Choice1.lower()
if Choice1 == 'new':
    dirL = input('Please enter the name of the directory ')
    bondsname = input('Please enter the filename for bonds ')
    partname = input('Please enter the filename for particles ')
    # partnamedf = input('Please enter the name of the file where to save partdf ')
    # bondnamedf = input('Please enter the name of the file where to save bonddf ')
    coordTcreate = input('Please enter the name of the file where to save info about broken bonds ')
    xBor,zBor = input('Please enter the borders of the object separated by comma ').split(',')
    xBor = float(xBor)
    #yBor = float(yBor)
    zBor = float(zBor)
    dataparticles = pd.read_csv(dirL + partname + ".txt",sep=' ', header=None)
    data = pd.read_csv(dirL + bondsname + ".txt",sep='\t', header=None)
    data = data.drop([0, 2, 5, 6, 8], axis='columns')
    data.set_index(data[1], drop=True, inplace=True)
    dataparticles.set_index(dataparticles[1], drop=True, inplace=True)
    dataparticles = dataparticles.drop([0, 1], axis='columns')
    print(data, dataparticles)


    def parsingPart(datapart):
        p = {}
        for j in datapart.index:
            t = {}
            for i in datapart.columns:
                if datapart[i][j] == 2:
                    t.update(
                        {datapart[i + 1][j]: np.array([datapart[i + 3][j]*1e+3, datapart[i + 4][j]*1e+3, datapart[i + 5][j]*1e+3])})
            p.update({j: t})
        df = pd.DataFrame(p).T
        print(df)
        return df


    def coordInfodf(data, datadf):
        col = np.array(datadf.columns)
        col = np.array([float(i) for i in col[1:]])
        num = float(col[1])
        activ = data[[9]].copy()
        l = int(f'{num:e}'.split('e')[-1])
        data[9] = round(data[9], abs(l))
        data = data[data[9] < col[len(col) - 1]]
        b = {}
        for i in data.index:
            t = {}
            for j in datadf.columns:
                if ((abs((datadf[j][data[3][i]][0] + datadf[j][data[4][i]][0]) / 2))**2 + ((datadf[j][data[3][i]][1] + datadf[j][data[4][i]][1]) / 2)**2 <= xBor**2) and (abs((datadf[j][data[3][i]][2] + datadf[j][data[4][i]][2]) / 2) <= zBor):
                    t.update({j: np.array([(datadf[j][data[3][i]][0] + datadf[j][data[4][i]][0]) / 2,
                                        (datadf[j][data[3][i]][1] + datadf[j][data[4][i]][1]) / 2,
                                        (datadf[j][data[3][i]][2] + datadf[j][data[4][i]][2]) / 2])})
            b.update({i: t})
        df = pd.DataFrame(b).T
        print(df)
        return df,data,activ


    def Broken_bonds(bondcoord, data,activ):
        bondcoord.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
        data = data[data.index.isin(bondcoord.index)]
        Finaldf = data[[9]].copy()
        Finaldf['Time'] = Finaldf[9]
        Finaldf = Finaldf.drop([9], axis='columns')


        Finaldf['X'] = np.array([bondcoord[Finaldf['Time'][i]][i][0] for i in bondcoord.index])
        Finaldf['Y'] = np.array([bondcoord[Finaldf['Time'][i]][i][1] for i in bondcoord.index])
        Finaldf['Z'] = np.array([bondcoord[Finaldf['Time'][i]][i][2] for i in bondcoord.index])
        Finaldf['Timeact'] = np.array([activ[9][i] for i in bondcoord.index])
        print(Finaldf.columns)
        Finaldf.sort_values(by='Time', ascending=True, inplace=True)
        print(Finaldf)
        Finaldf.to_csv(dirL + coordTcreate + '.csv')
        return Finaldf


    datapart = parsingPart(dataparticles)
    print(datapart)
    bondcoord,data,activ = coordInfodf(data, datapart)
    print(bondcoord)
    Final = Broken_bonds(bondcoord, data,activ)



Choice = input('Please enter the type of analysis, you would like to perform: if you want to finish enter stop , if you want to get defects on one step print 1 if you want to get defects on muliple steps print 2,if you want to get emission enter Em ')
Choice = Choice.lower()
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
        coordT.drop([5], axis=1, inplace=True)
        col1 = np.array([float(i) for i in coordT[1]])
        col2 = np.array([float(i) for i in coordT[2]])
        col3 = np.array([float(i) for i in coordT[3]])
        col4 = np.array([float(i) for i in coordT[4]])
        coordT[1] = col1
        coordT[2] = col2
        coordT[3] = col3
        coordT[4] = col4
    elif Choice1 == 'new':
        coordT = pd.read_csv(dirL + coordTcreate + ".csv", header=None)
        coordT.drop([0], axis=0, inplace=True)
        coordT.set_index(0, drop=False, inplace=True)

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
    defsdf.to_csv(dir + defSizename + str(Ftime) + '.csv')
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
        coordT.drop([5], axis=1, inplace=True)
        col1 = np.array([float(i) for i in coordT[1]])
        col2 = np.array([float(i) for i in coordT[2]])
        col3 = np.array([float(i) for i in coordT[3]])
        col4 = np.array([float(i) for i in coordT[4]])
        coordT[1] = col1
        coordT[2] = col2
        coordT[3] = col3
        coordT[4] = col4
    elif Choice1 == 'new':
        coordT = pd.read_csv(dirL + coordTcreate + ".csv", header=None)
        coordT.drop([0], axis=0, inplace=True)
        coordT.set_index(0, drop=False, inplace=True)
    #coordT.drop([0], axis=0, inplace=True)
    #coordT.set_index(0, drop=False, inplace=True)
    # print(coordT)
    Ftime = float(input('Please enter the final step '))
    r = float(input('Please enter the max distance '))
    step = int(input('Please enter the saving step '))


    def Get_defects_loop(coordT, Ftime, r, step, defSizename, defectsName):
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
    defects = Get_defects_loop(coordT, Ftime, r, step, defSizename, defectsName)



elif Choice == 'em':
    dir = input('Please enter the name of the directory ')
    defectsName = input('Please enter the name of the file where to save the defects ')
    defSizename = input('Please enter the name of the file where to save the sizes of the defects ')
    if Choice1 == 'exist':
        coordTname = input('Please enter the path for the file that contains info about broken bonds ')
        coordT = pd.read_csv(coordTname, header=None)
        coordT.drop([0], axis=0, inplace=True)
        coordT.set_index(0, drop=False, inplace=True)
        #coordT[1] = coordT[5]

        coordT.drop([5],axis = 1,inplace = True)
        col1 = np.array([float(i) for i in coordT[1]])
        col2 = np.array([float(i) for i in coordT[2]])
        col3 = np.array([float(i) for i in coordT[3]])
        col4 = np.array([float(i) for i in coordT[4]])
        coordT[1] = col1
        coordT[2] = col2
        coordT[3] = col3
        coordT[4] = col4
    elif Choice1 == 'new':
        coordT = pd.read_csv(dirL + coordTcreate + ".csv", header=None)
        coordT.drop([0], axis=0, inplace=True)
        coordT.set_index(0, drop=False, inplace=True)
    # coordT.drop([0], axis=0, inplace=True)
    # coordT.set_index(0, drop=False, inplace=True)
    # print(coordT)
    Ftime = float(input('Please enter the final step '))
    r = float(input('Please enter the max distance '))


    def Get_defects_loop(coordT, Ftime, r, defSizename, defectsName):
        coordT = coordT[coordT[1] <= Ftime]
        Timelist = [i for i in coordT[1].unique()]
        for j in range(0, len(Timelist)):
            time = Timelist[j]
            coordTi = coordT[coordT[1] == time]
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
            #np.save(dir + defectsName + '_' + str(Ftime) + '_' + str(time) + '.npy', defects)
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
            defsdf.to_csv(dir + defSizename + '_' + str(Ftime) + '_' + str(time) + '.csv')
            print('step_', time)
        return defects
    defects = Get_defects_loop(coordT, Ftime, r, defSizename, defectsName)
print('end')
end = input('Enter any letter ')