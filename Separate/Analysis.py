print(' If you want to analise Emission enter Em','\n',
      'for Defects on one step enter def1,','\n',
    'for Defects on multiple steps enter def2','\n',
      'for Emission by layers enter embl'
      )
Anchoice = input()

if Anchoice == 'em':
    import EmAnalysis