import pandas as pd
import numpy as np

dataparticles = pd.read_csv("D:\MUSEN Materials\Bigmodeldata\partexport.txt", sep=' ', header=None)
data = pd.read_csv("D:/MUSEN Materials/Bigmodeldata/bondexpactiv.txt", sep=' ', header=None)
data = data.drop([0, 2, 5, 6,8], axis='columns')
data.set_index(data[1], drop=True, inplace=True)
dataparticles.set_index(dataparticles[1], drop=True, inplace=True)
dataparticles = dataparticles.drop([0, 1], axis='columns')
print(data,dataparticles)
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
    return df

datapart = parsingPart(dataparticles)
print((datapart))
col = np.array(datapart.columns)
col = np.array([float(i) for i in col[1:]])
num = float(col[1])
l= int(f'{num:e}'.split('e')[-1])
data[9] = round(data[9],abs(l))
data = data[data[9] < col[len(col) - 1]]
print(datapart.columns[28])

print(data.index)
b = {}

for i in data.index:
    #print(datapart[data[9][i]][data[3][i]])
    print(i)
    b.update({i:[data[9][i],(datapart[data[9][i]][data[3][i]][0] + datapart[data[9][i]][data[4][i]][0])/2,(datapart[data[9][i]][data[3][i]][1] + datapart[data[9][i]][data[4][i]][1])/2,(datapart[data[9][i]][data[3][i]][2] + datapart[data[9][i]][data[4][i]][2])/2]})
    Bdf = pd.DataFrame.from_dict(b).T
print(Bdf)
Bdf.to_csv("D:\MUSEN Materials\Bigmodeldata\Bdf.csv")