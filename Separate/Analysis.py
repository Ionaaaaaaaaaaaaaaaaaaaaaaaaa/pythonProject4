print(' If you want to analise Emission enter Em','\n',
      'for Defects on one step enter def1,','\n',
    'for Defects on multiple steps enter def2','\n',
      'for Emission by layers enter embl'
      )
Anchoice = input()

if Anchoice == 'em':
    import EmAnalysis
if Anchoice == 'def1':
    import DefAnalysis
if Anchoice == 'def2':
    import DefMultiAnalysis
if Anchoice == 'embl':
    import Emission_by_LayersAnalysis
