import DefAnalysis as def1A
import DefMultiAnalysis as def2A
import EmAnalysis as EMA
import Emission_by_LayersAnalysis as emblA

def launch():
    print(' If you want to analise Emission enter EmA', '\n',
          'for Defects on one step enter def1A,', '\n',
          'for Defects on multiple steps enter def2A', '\n',
          'for Emission by layers enter emblA'
          )
    Anchoice = input('==>')
    Anchoice = Anchoice.lower()
    if Anchoice == 'ema':
        EMA.start()
    if Anchoice == 'def1a':
        def1A.start()
    if Anchoice == 'def2a':
        def2A.start()
    if Anchoice == 'embla':
        emblA.start()