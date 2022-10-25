import Get_defects_on_one_step as Gd1
import  Broken_Bonds as BB
import Get_defects_on_multiple_steps as Gd2
import Emission as EM
import Emission_by_layers as embl
import Analysis as An
def launch ():
    print('If you want to create a file with broken bonds enter BB.','\n',
                     'To get defects on one step enter Gd1.','\n',
                     'To get defects on multiple steps enter Gd2.','\n',
                     'To get Emission enter em.','\n',
                     'To get Emission by layers enter embl.','\n',
          'To start Analysis enter An')
    LaunchChoice = input('==>')
    LaunchChoice = LaunchChoice.lower()
    if LaunchChoice == 'bb':
        BB.start()
    elif LaunchChoice == 'gd1':
        Gd1.start()
    elif LaunchChoice == 'gd2':
        Gd2.start()
    elif LaunchChoice == 'em':
        EM.start()
    elif LaunchChoice == 'embl':
        embl.start()
    elif LaunchChoice == 'an':
        An.launch()
launch()