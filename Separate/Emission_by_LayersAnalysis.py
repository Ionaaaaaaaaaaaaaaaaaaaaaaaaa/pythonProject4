import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
from sklearn.metrics import r2_score
import pickle
dir = input('Please enter the directory where to get files ') + '\_'
dir2 = input('Please enter the directory where to save files ') + '\_'
layer = input('Please enter the layer')
defectsdict = pickle.load(open(dir + layer + 'defectsdict.p','rb'))
defsizedict = pickle.load(open(dir + layer + 'defsizedict.p','rb'))

print('defectsdict keys-----------------------','\n',defectsdict.keys())

print('defsizedict-----------------------','\n',defsizedict.keys())


def funcexp(x, a, b):
    return a * np.exp(-b * x)


def funcpower(x, a, b):
    return a * (x ** -b)
Stats = {}
for time in defsizedict.keys():
    m = defsizedict[time]
    print(m)
    n = defectsdict[time]
    Maxdef = m['Size'].idxmax(axis=0)
    maxdefinfo = [n[i][Maxdef] for i in n.columns]
    Maxdefinfodf = pd.DataFrame(maxdefinfo, columns=['bond', 'X', 'Y', 'Z'])
    Maxdefinfodf.set_index('bond', inplace=True)
    Maxdefinfodf.to_csv(dir2 + 'Maxdefinfodf_' + str(time) + '.csv')
    print('maxdefect_', time, Maxdefinfodf)
    # print(m)
    counts = m['Size'].value_counts(sort=True)
    counts = pd.DataFrame(counts)
    counts.sort_index(inplace=True)
    counts.index.name = 'Size'
    counts['N'] = counts['Size']
    counts.drop(['Size'], axis='columns', inplace=True)
    print('Counts_', time, counts)
    counts.to_csv(dir2 + 'Counts_' + str(time) + '.csv')

    if len(counts.index) >= 3:
        # try:
        index = np.array([i for i in counts.index])
        data = np.array([i for i in counts['N']])
        popt, pcov, infodict, mesg, ier = curve_fit(f=funcexp, xdata=index, ydata=data, full_output=True, maxfev=5000)
        res = stats.linregress(data, funcexp(index, *popt))
        rsquared = res.rvalue ** 2
        print(data, funcexp(index, *popt))
        r_sq = r2_score(data, funcexp(index, *popt))
        print('Exponential  ', rsquared)
        print('Exponential  2', r_sq)

        x = np.linspace(min(index), max(index), 1000)

        # except Exception:
        # pass

        # try:
        popt1, pcov1, infodict1, mesg1, ier1 = curve_fit(f=funcpower, xdata=index, ydata=data, full_output=True)
        res2 = stats.linregress(data, funcpower(index, *popt1))
        rsquared2 = res2.rvalue ** 2
        print('Power  ', rsquared2)
        x = np.linspace(min(index), max(index), 1000)
        if time <= 0.008:
            # 0.0039999999999999975
            plt.figure()
            plt.subplot(1, 2, 1)
            plt.loglog(x, funcpower(x, *popt1), 'r-', label='power_log')
            plt.loglog(x, funcexp(x, *popt), 'r-', label='Exp_log', c='b')
            plt.loglog(counts, label='Counts_log')
            plt.legend()
            # plt.show()
            plt.subplot(1, 2, 2)
            plt.plot(x, funcpower(x, *popt1), 'r-', label='power')
            plt.plot(x, funcexp(x, *popt), 'r-', label='Exp', c='b')
            plt.plot(counts, label='Counts')
            plt.title(time)
            plt.legend()
            # plt.show()
        # except Exception:
        # pass
        Stats.update({time: [rsquared, rsquared2, max(index), sum(data)]})
    else:
        Stats.update({time: ['--', '--', max(counts.index), sum(counts['N'])]})

    print('step_save_', time)
Statsdf = pd.DataFrame.from_dict(Stats,orient='index',columns=['ExpRsq','PowerRsq','Max_size','N_defects'])
Statsdf.index.name = 'Time'
print(Statsdf)
Statsdf.to_csv(dir2 + 'Stats.csv')