import pandas as pd
import numpy as np
dir = input('Please enter the name of the directory ')
bondsname = input('Please enter the filename for bonds ')
partname = input('Please enter the filename for particles ')
partnamedf = input('Please enter the name of the file where to save partdf ')
bondnamedf = input('Please enter the name of the file where to save bonddf ')
coordT = input('Please enter the name of the file where to save info about broken bonds ')
data = pd.read_csv(dir + bondsname + ".txt",sep=' ',header=None)
datapart = pd.read_csv(dir + partname + ".txt",sep = ' ',header=None)
data = data.drop([2,5,6], axis='columns')
datapart.set_index(datapart[1], drop=True,inplace=True)
datapart = datapart.drop([0,1], axis='columns')
print (data)
print (datapart)
def get_dataInd_and_Col (data):

    I = [i for i in data.index]
    C = [i for i in data.columns]
    return I,C
def parsingPart(datapart):
    p = {}
    for j in datapart.index:
        t = {}
        for i in datapart.columns:
            if datapart[i][j] == 2:
                t.update({datapart[i+1][j]:np.array([datapart[i+3][j],datapart[i+4][j],datapart[i+5][j]])})
        p.update({j:t})
    df = pd.DataFrame(p).T
    print(df)
    df.to_csv(dir + partnamedf  + ".csv")
    return df

def coordInfodf (data, datadf):
    b = {}
    for i in data.index:
        t = {}
        for j in datadf.columns:
            t.update({j:np.array([(datadf[j][data[3][i]][0] + datadf[j][data[4][i]][0])/2,(datadf[j][data[3][i]][1] + datadf[j][data[4][i]][1])/2,(datadf[j][data[3][i]][2] + datadf[j][data[4][i]][2])/2])})
        b.update({i:t})
    df = pd.DataFrame(b).T
    print(df)
    df.to_csv(dir + bondnamedf + ".csv")
    return df

def brokenbondstimes (data,bonddf):
    b = {}
    used = np.array([])
    I,C = get_dataInd_and_Col(data)
    for i in range(0,len(I)):
        for j in range(0,len(C)):
            if data[C[j - 1]][I[i]] not in used:
                if data[C[j]][I[i]] == 18 and data[C[j + 1]][I[i]] == 0 and I[i] not in used and data[C[j-1]][I[i]] !=0:
                    b.update({data[C[j-1]][I[i]]:np.array([I[i]])})
                    used = np.append(used,data[C[j-1]][I[i]])
                    used = np.append(used,I[i])
            else:
                if data[C[j]][I[i]] == 18 and data[C[j + 1]][I[i]] == 0 and I[i] not in used and data[C[j-1]][I[i]] !=0:
                    b[data[C[j-1]][I[i]]] = np.append(b[data[C[j-1]][I[i]]],I[i])
                    used = np.append(used,I[i])
    co = {}
    bk = [i for i in b.keys()]
    bk = sorted(bk)
    print(bk)
    for i in bk:
        for j in b[i]:
            co.update({j: [i, bonddf[i][j][0], bonddf[i][j][1], bonddf[i][j][2]]})

    df = pd.DataFrame(co).T
    print (df)
    df.to_csv(dir + coordT + ".csv")
    #np.save("D:/MUSEN Materials/Musen export/dictopt.npy", b)
    #np.savetxt("D:/MUSEN Materials/Musen export/dictopt.txt", b)
    return b,df
partdf = parsingPart(datapart)
bonddf = coordInfodf(data,partdf)
b,TBonddf = brokenbondstimes(data,bonddf)
#print (b[0.006])
#bondtimesdf

