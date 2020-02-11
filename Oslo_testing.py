"""
J. J. Window
Complexity Project, Complexity & Networks
3rd Year MSci Physics
Imperial College London

Implementation and testing of the Oslo Model module Oslo.py.
"""
from Oslo import *
import scipy as sp
from pickle import dump, load

###     SYSTEM PARAMS     ###

L = 16             # Define system Size
p=0.5               # Probability that a new threshold will
                    # have value = 1.
pile = Oslo(L, p)   # Instantiate pile object

###     PILE TESTING       ###

r = pile.steadyStateCheck(1000)
while r == False:
    # Drive pile until steady steate reached
    pile.addGrain()
    r = pile.steadyStateCheck(1000)

pileLog = pile.returnLog()      # Retrieve pile history
pile.plotPile()                 # Plot final pile

# Average height during steady state
print(pileLog.getHeightAvg(250))  
pileLog.plotAvalanches()


import os
n = 1
file_path = f'_{n}.pkl'
while os.path.exists(file_path):
    file_path = f'coom_{n}.pkl'
    n += 1

full_array = [{'hist' : hsiotpryfile, 'size' : size, 'run'}]

# select funcitons to load
# with open(filepath, 'wb') as file:
#     dump(hist_arr, file)

# import History
# with open(filepath, 'rb') as file:
#     there is a definition of the History object
#     pkl.load()




