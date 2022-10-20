import pandas as pd
import numpy as np


dirL = input('Please enter the name of the directory ')
bondsname = input('Please enter the filename for bonds ')
partname = input('Please enter the filename for particles ')
# partnamedf = input('Please enter the name of the file where to save partdf ')
# bondnamedf = input('Please enter the name of the file where to save bonddf ')
coordTcreate = input('Please enter the name of the file where to save info about broken bonds ')
dir2 = input('Please enter the name of the directory where to save the file containing broken bonds ')
xBor,zBor = input('Please enter the borders of the object separated by comma ').split(',')
xBor = float(xBor)
#yBor = float(yBor)
zBor = float(zBor)
dataparticles = pd.read_csv(dirL + partname + ".txt",sep=' ', header=None)
data = pd.read_csv(dirL + bondsname + ".txt",sep=' ', header=None)
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
        #data = data[data[9] <= col[len(col) - 1]]
        data = data[data[9] <= col[len(col)]]
        b = {}
        for i in data.index:
            t = {}
            for j in datadf.columns:
                #if (((datadf[j][data[3][i]][0] + datadf[j][data[4][i]][0]) / 2)**2 + ((datadf[j][data[3][i]][1] + datadf[j][data[4][i]][1]) / 2)**2 <= xBor**2) and (abs((datadf[j][data[3][i]][2] + datadf[j][data[4][i]][2]) / 2) <= zBor):
                t.update({j: np.array([(datadf[j][data[3][i]][0] + datadf[j][data[4][i]][0]) / 2,
                                        (datadf[j][data[3][i]][1] + datadf[j][data[4][i]][1]) / 2,
                                        (datadf[j][data[3][i]][2] + datadf[j][data[4][i]][2]) / 2])})
            b.update({i: t})
        df = pd.DataFrame(b).T
        print(df)
        return df,data,activ


def Broken_bonds(bondcoord, data,activ):
        bondcoord.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
        print(bondcoord)
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
        Finaldf = Finaldf[((Finaldf['X']**2 + Finaldf['Y']**2)<=xBor**2)&(Finaldf['Z']<=zBor)]
        print(Finaldf)
        Finaldf.to_csv(dir2 + coordTcreate + '.csv')
        return Finaldf


datapart = parsingPart(dataparticles)
print(datapart)
bondcoord,data,activ = coordInfodf(data, datapart)

print(bondcoord)
Final = Broken_bonds(bondcoord, data,activ)