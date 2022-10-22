def launch ():
    print('If you want to create a file with broken bonds enter BB.','\n',
                     'To get defects on one step enter Gd1.','\n',
                     'To get defects on multiple steps enter Gd2.','\n',
                     'To get Emission enter em.','\n',
                     'To get Emission by layers enter embl.')
    LaunchChoice = input()
    LaunchChoice = LaunchChoice.lower()
    if LaunchChoice == 'bb':
        import Broken_Bonds as BB
        Launch = BB
    elif LaunchChoice == 'gd1':
        import Get_defects_on_one_step as Gd1
        Launch = Gd1
    elif LaunchChoice == 'gd2':
        import Get_defects_on_multiple_steps as Gd2
        Launch = Gd2
    elif LaunchChoice == 'em':
        import Emission as em
        Launch = em
    elif LaunchChoice == 'embl':
        import Emission_by_layers as embl
        Launch = embl
Launch_programm = launch()