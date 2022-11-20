import pandas as pd

def get_minvalue(inputlist):
    # get the minimum value in the list
    min_value = min(inputlist)

    # return the index of minimum value
    min_index = inputlist.index(min_value)
    return min_index

with open(r"D:\MUSEN Materials\granit cylinder_various_grains_various_bonds\Bonds.txt", encoding='utf8') as f:
    lines = f.readlines()
    print(lines[0].split())
    sb = ['='for i in range (0,100)]
    [print(i,end='') for i in sb]
    print()
    Bonds = {}
    l = len(lines)
    n = l/100
    s = 0
    it = 0
    rBor = 5.3
    zBor = 10.3
    for j in lines:
        spltline = j.split()
        coordTime = {}
        if it >= s-0.5 and it <= s+0.5:
            print('=',end='')
            s+=n
        it += 1
        #print(spltline)
        [coordTime.update({float(spltline[i+1]):[float(spltline[i+3])*1e3,float(spltline[i+4])*1e3,float(spltline[i+5])*1e3]}) for i in range(10,len(spltline)) if spltline[i] == '2' if i <=len(spltline) - 6]
        DeathT = [float(spltline[i+2]) for i in range(0,20) if spltline[i] == '24']
        #print(DeathT[0])
        #print([abs(i - DeathT[0]) for i in coordTime.keys()])
        key = [j for j in coordTime.keys()][get_minvalue([abs(i - DeathT[0]) for i in coordTime.keys()])]
        #print(key)
        Bonds.update({int(spltline[1]):[key] + coordTime[key]})
    print(Bonds)
    bondsdf = pd.DataFrame.from_dict(Bonds,orient='index', columns=['TDeath','X', 'Y', 'Z'])
    bondsdf = bondsdf[((bondsdf['X'] ** 2 + bondsdf['Y'] ** 2) <= rBor ** 2) & (bondsdf['Z'] <= zBor)]
    bondsdf = bondsdf[(bondsdf['TDeath'] < 0.0159)&(bondsdf['TDeath'] > 0)]
    bondsdf.index.name = 'Bonds'
    print(bondsdf)
    bondsdf.to_csv("D:\MUSEN Materials\granit cylinder_various_grains_various_bonds" + '\Bonds2' + '.csv')
f.close()
