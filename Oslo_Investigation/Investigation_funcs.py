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
from scipy.optimize import curve_fit

allDicts = []
num_runs = 5    # change to 10 for new datalogs
num_lengths = 7

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

def getLogsArray(run):
    # Make array of the datalog objects for any run of each size
    logsArray = [allDicts[i][run]['Log'] for i in range(0, 7)]
    return logsArray

def plotHeightwithTime(logsArray):
    heightsArray = []
    plt.xlabel('Number of Drives')
    plt.ylabel('Pile Height')
    for i in range(0, num_lengths):
        _heights = logsArray[i].getHeightsList()
        heightsArray.append(_heights)
        n = 2**(i+2)
        plt.plot(range(len(_heights)), _heights, label = f'L = {n}', linewidth = 0.75)
    plt.legend()
    plt.show()
    return heightsArray

def Q2_a():
    logsArray = getLogsArray(0)
    plotHeightwithTime(logsArray)
    return None

### 2b ###

def firstExitAllSizes(logsArray):
    firstExit = []
    for log in logsArray:
        totalGrains = [log.getNumGrains(i) for i in range(log.getNumDrives())]
        exitIdx = [idx for idx, numArr in enumerate(zip(totalGrains, totalGrains[1:])) if numArr[0] >= numArr[1]]
        firstExit.append(exitIdx[0])
    return firstExit

def t_c_avg(plot = False):
    all_runs = [getLogsArray(run) for run in range(num_runs)] 
    _exits = [firstExitAllSizes(log) for log in all_runs]
    # Calculate mean value of critical drive number for each size pile
    exit_means = [np.mean([_exits[i][j] for i in range(num_runs)]) for j in range(num_lengths)]
    if plot == True:
        # Plot all sizes
        L = [2**n for n in range(2, 9)]
        plt.xlabel('System Size')
        plt.ylabel('t_c')
        plt.title("All System Sizes")
        plt.plot(L, exit_means, color = 'red')
        plt.show()
        # Plot L>>1, fit guess function.
        # L_ = [2**n for n in range(4, 9)]
        # def exp_fit(L, A, b):
        #     # exponential modelling function to be optimised.
        #     return A*np.exp(b * (L))
        # # popt, pcov = curve_fit(exp_fit, L_, exit_means[2:], [0.5, 0.01])
        # plt.xlabel('System Size')
        # plt.ylabel('t_c')
        # plt.title("System Sizes L >> 1")
        # plt.plot(L_, exit_means[2:], '+', color = 'black')
        # x = np.linspace(16, 256, 500)
        # plt.plot(x, [exp_fit(_x, popt[0], popt[1]) for _x in x], color = 'red')
        # plt.show()
    return exit_means

### 2c ###

def h_mean():

    logs = [getLogsArray(run) for run in range(num_runs)]
    """
    logs :
    L =      _____4_______8__...__256__
    RUN 0   |  [h_4_0] [h_8_0] ...
        1   |  [h_4_1] ...
        2   |
        ... |
        10  |
    """
    logs = np.asarray(logs)
    logs_T = logs.T
    mean_heights = []
    for i in range(num_lengths):
        avg_h = np.mean([logs_T[i][j].getHeightsList() for j in range(num_runs)], axis = 0)
        mean_heights.append(avg_h)

    plt.plot(range(len(mean_heights[-1])), mean_heights)

    ### Fucking figure it out


