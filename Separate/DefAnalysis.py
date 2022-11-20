import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
from sklearn.metrics import r2_score
import pickle


def funcexp(x, a, b):
    return a * np.exp(-b * x)


def funcpower(x, a, b):
    return a * (x ** -b)

def analysis(dir2,defects,defectsdf,defsdf,r,Bord1,Bord2,plots):
        Stats = {}
        Maxdef = defsdf['Size'].idxmax(axis=0)
        maxdefinfo = [defectsdf[i][Maxdef] for i in defectsdf.columns]
        Maxdefinfodf = pd.DataFrame(maxdefinfo, columns=['bond', 'X', 'Y', 'Z'])
        Maxdefinfodf.set_index('bond', inplace=True)
        Maxdefinfodf.to_csv(dir2 + 'Maxdefinfodf_.csv')
        print('maxdefect_', Maxdefinfodf)

        counts = defsdf['Size'].value_counts(sort=True)
        counts = pd.DataFrame(counts)
        counts.sort_index(inplace=True)
        counts.index.name = 'Size'
        counts['N'] = counts['Size']
        counts.drop(['Size'], axis='columns', inplace=True)
        print('Counts_', counts)
        counts.to_csv(dir2 + 'Counts.csv')
        counts = counts[(counts.index >= Bord1) & (counts.index <= Bord2)]
        counts.to_csv(dir2 + '' + str(Bord1) + '-' + str(Bord2) + 'Counts.csv')

        if len(counts.index) >= 3:
                # try:
                index = np.array([i for i in counts.index])
                data = np.array([i for i in counts['N']])
                popt, pcov, infodict, mesg, ier = curve_fit(f=funcexp, xdata=index, ydata=data, full_output=True,
                                                            maxfev=5000)
                res = stats.linregress(data, funcexp(index, *popt))
                rsquared = res.rvalue ** 2
                print(data, funcexp(index, *popt))
                r_sq = r2_score(data, funcexp(index, *popt))
                print('Exponential  ', rsquared)
                print('Exponential  2', r_sq)

                x = np.linspace(min(index), max(index), 1000)

                popt1, pcov1, infodict1, mesg1, ier1 = curve_fit(f=funcpower, xdata=index, ydata=data, full_output=True)
                res2 = stats.linregress(data, funcpower(index, *popt1))
                rsquared2 = res2.rvalue ** 2
                print('Power  ', rsquared2)
                Stats.update({1: [rsquared, rsquared2, max(index), sum(data)]})
        Statsdf = pd.DataFrame.from_dict(Stats, orient='index', columns=['ExpRsq', 'PowerRsq', 'Max_size', 'N_defects'])
        Statsdf.index.name = 'Time'
        print(Statsdf)
        Statsdf.to_csv(dir2 + 'Stats.csv')
        if plots == 'y':
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
                        ax.scatter(X[i], Y[i], Z[i], s=r * 10)
                plt.show()

def start():
        dir = input('Please enter the directory where to get files ') + '\_'
        dir2 = input('Please enter the directory where to save files ') + '\_'
        defects = pickle.load(open(dir + 'defects.p', 'rb'))
        defectsdf = pickle.load(open(dir + 'defectsdict.p', 'rb'))
        defsdf = pickle.load(open(dir + 'defsizedict.p', 'rb'))
        r = float(input('Enter radius for points '))
        Bord1 = float(input('Please enter the lower limit for the counts '))
        Bord2 = float(input('Please enter the upper limit for the counts '))
        plots = input('To draw plots enter y, otherwise n')
        plots = plots.lower()
        analysis(dir2, defects, defectsdf, defsdf, r, Bord1, Bord2,plots)
        print('end')
        input('Press any key')