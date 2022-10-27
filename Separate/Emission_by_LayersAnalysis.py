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
def Analysis(dir2,defectsdictGlobal,defsizedictGlobal,Bord1,Bord2,plots):
    for i in defectsdictGlobal.keys():
        defsizedict = defsizedictGlobal[i]
        defectsdict = defectsdictGlobal[i]
        print('==========================','_Layer' + str(i),'========================')
        Stats = {}
        for time in defsizedict.keys():
            m = defsizedict[time]
            print(m)
            n = defectsdict[time]
            Maxdef = m['Size'].idxmax(axis=0)
            maxdefinfo = [n[i][Maxdef] for i in n.columns]
            Maxdefinfodf = pd.DataFrame(maxdefinfo, columns=['bond', 'X', 'Y', 'Z'])
            Maxdefinfodf.set_index('bond', inplace=True)
            Maxdefinfodf.to_csv(dir2 + '_Layer' + str(i) + '_' + 'Maxdefinfodf_' + str(time) + '.csv')
            print('maxdefect_', time, Maxdefinfodf)
            # print(m)
            counts = m['Size'].value_counts(sort=True)
            counts = pd.DataFrame(counts)
            counts.sort_index(inplace=True)
            counts.index.name = 'Size'
            counts['N'] = counts['Size']
            counts.drop(['Size'], axis='columns', inplace=True)
            counts.to_csv(dir2 + '_Layer' + str(i) + '_' + 'T_' + str(time) + '_Counts.csv')
            counts = counts[(counts.index >= Bord1) & (counts.index <= Bord2)]
            counts.to_csv(dir2 + '_Layer' + str(i) + '_' + '' + str(Bord1) + '-' + str(Bord2) + 'T_' + str(time) + '_Counts.csv')
            print('Counts_', time, counts)

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

                # except Exception:
                # pass

                # try:
                popt1, pcov1, infodict1, mesg1, ier1 = curve_fit(f=funcpower, xdata=index, ydata=data, full_output=True)
                res2 = stats.linregress(data, funcpower(index, *popt1))
                rsquared2 = res2.rvalue ** 2
                print('Power  ', rsquared2)
                x = np.linspace(min(index), max(index), 1000)
                if plots == 'y':
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
                    plt.show()
                # except Exception:
                # pass
                Stats.update({time: [rsquared, rsquared2, max(index), sum(data)]})
            else:
                Stats.update({time: ['--', '--', max(counts.index), sum(counts['N'])]})

            print('step_save_', time)
        Statsdf = pd.DataFrame.from_dict(Stats, orient='index', columns=['ExpRsq', 'PowerRsq', 'Max_size', 'N_defects'])
        Statsdf.index.name = 'Time'
        print(Statsdf)
        Statsdf.to_csv(dir2 + '_Layer' + str(i) + '_' + 'Stats.csv')

def start():
    dir = input('Please enter the directory where to get files ') + '\_'
    dir2 = input('Please enter the directory where to save files ') + '\_'
    defectsdictGlobal = pickle.load(open(dir + 'defectsdict.p', 'rb'))
    defsizedictGlobal = pickle.load(open(dir + 'defsizedict.p', 'rb'))
    Bord1 = int(input('Please enter the lower limit for the counts '))
    Bord2 = int(input('Please enter the upper limit for the counts '))
    plots = input('To draw plots enter y, otherwise n')
    plots = plots.lower()
    print('defectsdict keys-----------------------', '\n', defectsdictGlobal.keys())

    print('defsizedict-----------------------', '\n', defsizedictGlobal.keys())
    Analysis(dir2, defectsdictGlobal, defsizedictGlobal, Bord1, Bord2,plots)
    print('end')
    input('Press any key ')