"""
J. J. Window
Complexity Project, Complexity & Networks
3rd Year MSci Physics
Imperial College London

Investigation of the Oslo model. 
"""
import numpy as np
from Oslo import *
import matplotlib.pyplot as plt

allDicts = []

for i in range(2, 9):
    n = 2**i
    with open(f'Oslo_Investigation/Final_runs/Oslo_{n}.npy', 'rb') as file:
        allDicts.append(np.load(file, allow_pickle=True))

"""
allDicts is of form:

[ {'Pile' : pile_obj, 'size' = 4, ...}, 
  {..., 'size' = 8, ...              }  
   ...                      { = 256, } ]
"""
### 2a ###
def Q2_a():
    # Make array of the datalog objects for the first run of each size
    logsArray = [allDicts[i][0]['Log'] for i in range(0, 7)]

    heightsArray = []
    plt.xlabel('Number of Drives')
    plt.ylabel('Pile Height')
    for i in range(0, 7):
        _heights = logsArray[i].getHeightsList()
        heightsArray.append(_heights)
        n = 2**(i+2)
        plt.plot(range(len(_heights)), _heights, label = f'L = {n}', linewidth = 0.75)
    plt.legend()
    plt.show()
    return heightsArray

### 2b ###

def Q2_b():
    firstExit = []
    for log in logsArray:
        totalGrains = [log.getNumGrains(i) for i in range(log.getNumDrives())]
        exitIdx = [idx for idx, numArr in enumerate(zip(totalGrains, totalGrains[1:])) if numArr[0] >= numArr[1]]
        firstExit.append(exitIdx[0])

    return firstExit

### 2c ###
