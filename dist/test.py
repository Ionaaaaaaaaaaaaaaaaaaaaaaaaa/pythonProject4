import pandas as pd
coordTname = input('Please enter the path for the file that contains info about broken bonds ')
coordT = pd.read_csv(coordTname, header=0,index_col=0)
print(coordT)