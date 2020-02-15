"""
J. J. Window
Complexity Project, Complexity & Networks
3rd Year MSci Physics
Imperial College London

Oslo Model class module. Contains classes for a ricepile follwing
the Oslo model algorithm, as well as a Datalog class for storing the
history of the pile for interrogation.
"""
import numpy as np
from random import choice
from random import random
import copy
import matplotlib.pyplot as plt
import os
from pickle import dump, load

class Datalog:
    """
    Object class to save all iterations of the ricepile in arrays which can later be 
    accessed. Needs pile dimension L and threshold selection probability p to instantiate.

    Methods:
    add(newHeights, newGrads, newTholds) - appends the provided height, gradient and threshold 
                                           arrays to the object.
    getSnapshot(n)                       - returns a tuple of arrays containing values of heights, 
                                           gradients and thresholds for the pile after drive n.
    getFullHist()                        - returns tuple of arrays containing all snapshots.
    """
    def __init__(self, L, p):
        self.L = L
        self.p = p
        self.pileLog = []
        # self.gradsLog = []
        self.tholdsLog = []
        self.avalsLog = []

    def add(self, newHeights, newGrads, newTholds, newAvalanche):
        """
        Adds new data to class attributes.
        """
        self.pileLog.append(copy.copy(newHeights))
        # self.gradsLog.append(copy.copy(newGrads))
        self.tholdsLog.append(copy.copy(newTholds))
        self.avalsLog.append(copy.copy(newAvalanche))

    def getSnapshot(self, n):
        """
        Returns the nth instance of the datalog - i.e, a snapshot of the pile after drive n.
        """
        if type(n) is not int:
            raise TypeError("n parameter must be an integer.")
        # return (self.pileLog[n], self.gradsLog[n], self.tholdsLog[n], self.avalsLog[n])
        return (self.pileLog[n], self.tholdsLog[n], self.avalsLog[n])

    def plotSnapshot(self, n):
        """
        Plots the nth snapshot of the pile. Passing n = -1 will plot the final state of the 
        pile. Displays bar chart and returns dictionary of snapshot properties.
        """
        if type(n) is not int:
            raise TypeError("n parameter must be an integer.")

        # p, g, t, a = self.getSnapshot(n)
        p, t, a = self.getSnapshot(n)
        plt.bar(range(0, self.L), p, width = 1, align = 'edge')
        plt.show()
        # return {'Pile' : p, 'Gradients' : g, 'Thresholds' : t, 'Avalanche Sizes' : a}
        return {'Pile' : p, 'Thresholds' : t, 'Avalanche Sizes' : a}

    def getFullHist(self):
        """
        Returns all class attributes in full.
        """
        # return (self.pileLog, self.gradsLog, self.tholdsLog, self.avalsLog)
        return (self.pileLog, self.tholdsLog, self.avalsLog)

    def getNumGrains(self, n):
        """
        Returns number of grains in the system at any frame 'n'.
        """
        if type(n) is not int:
            raise TypeError("n parameter must be an integer.")
        
        return sum(self.pileLog[n])

    def getHeightsList(self):
        """
        Returns the array of the pile height after each drive.
        In this case, height is defined at the number of grains 
        at site 0, or equivalently as the sum of all the gradients 
        in the pile.
        """
        # # Below relies on saving gradsLog. To save storage so arrays can be saved using pkl, this is discarded.
        # return [sum(self.gradsLog[i]) for i in range(0, self.L)]
        return [pile[0] for pile in self.pileLog]

    def getHeightAvg(self, n):
        """
        Returns average pile height for n most recent drives.
        """
        heightsList = self.getHeightsList()
        return np.mean(heightsList[-n:])

    def getAvalSizes(self):
        """
        Returns array of avalanche sizes for all system drives.
        """
        return self.avalsLog

    def getNumDrives(self):
        """
        Returns number of drives performed on the system
        """
        return len(self.avalsLog)

    def plotAvalanches(self):
        """
        Plots the sizes of all avalanches.
        """
        plt.bar(*list(zip(*enumerate(self.avalsLog))), width=1, align = 'edge')
        plt.show()

    def plotHeight(self, plot = False):
        """
        Plots individual height graph if plot == True. Returns (num. drives, pile height) as
        tuple of arrays.
        """
        h = []
        for pile in self.pileLog:
            h.append(pile[0])
        if plot == True:
            plt.xlabel('Number of Drives')
            plt.ylabel('Pile height')
            plt.plot(range(len(h)), h, color = 'red')
            plt.show()
        return (range(len(h)), h)

    def getGrads(self, n):
        """
        Returns nth snapshot of gradients from pile heights.
        """
        z = [i-j for i, j in zip(self.pileLog[-1] self.pileLog[-1][1:])]
        # Gradient of last site is simply its height
        z.append(self.pileLog[-1][-1])
        return z
        


class Oslo:
    @staticmethod    
    def thold_gen(p):
        """
        Generates a new threshold value for a given site. Can be called at
        initialisation or relaxation. Parameter p is the probability a site
        gets a threshold value of 1. A threshold value of 2 has an associated 
        probability of (1-p).
        """
        thold_vals = [1,2]
        z_th = np.random.choice(thold_vals, p = [p, 1-p])
        return z_th

    def __init__(self, L, p):
        # Check arguments are valid
        L = int(L)
        if type(p) is not float:
            raise TypeError("Argument p must be of type float")
        if (p<0) or (p>1):
            raise Exception("Argument p must be a valid probability 0 <= p <= 1")

        self.L = L                                      # Size of system
        self.p = p                                      # Prob of choosing z_th = 1 at relaxation
        self.exitNum = 0  
        self.exitArray = []                             # Number of grains out of system          
        self.N = 0                                      # Number of grains added to system
        self.dataLog = Datalog(self.L, self.p)          # Instance of datalog

        # Initialise pile with empty sites
        self.pile = np.zeros(L) 
        # Define gradients from i = 0 to L-1
        self.z = [i-j for i, j in zip(self.pile, self.pile[1:])]
        # Add i=L gradient (0 at initialisation)
        self.z.append(0)
        self.z_th = [self.thold_gen(self.p) for _ in range(0, self.L)]

    def update_z(self):
        """
        Changes values of gradient after a drive/relaxation.
        """
        self.z = [i-j for i, j in zip(self.pile, self.pile[1:])]
        # Gradient of last site is simply its height
        self.z.append(self.pile[-1])

    def drive(self):
        """
        Adds a 'grain' to the leftmost site of the pile.
        """
        self.pile[0] += 1
        self.N += 1
        self.update_z()

    def relax(self):
        """
        Relaxes the pile after a drive has been performed. Iterates
        through the pile checking the gradient at each site. If the gradient
        is greater than the threshold, the grain topples to the next site
        and the surrounding gradients are altered. This continues until the
        whole pile has been checked without needing to perform a relaxation.
        """
        completePass = False
        exited = 0
        avalSize = 0
        while completePass == False:
            # Counts how many sites have been evaluated without
            # a relaxation needed.
            noRelax = 0
            # Loop through all sites
            for i, _z in enumerate(self.z):
                # Check if site has gradient > threshold
                relax = bool(_z>self.z_th[i])
                # Check if loop is at beginning or end
                A = bool(i == 0)
                B = bool(i == self.L-1)
                
                if relax:
                    # If a relaxation is needed, reset to 0.
                    noRelax = 0
                    # And increase avalance size by 1 site.
                    avalSize += 1
                    # Remove grain from site
                    self.pile[i] -= 1
                    # Check if site is first or last and apply
                    # relaxation algorithm accordingly
                    if A:
                        self.z[i] -=2
                        self.z[i+1] += 1
                        # Add grain to next site
                        self.pile[i+1] += 1
                    elif B:
                        self.z[i] -= 1
                        self.z[i-1] += 1
                        # Increase count of grains leaving system
                        self.exitNum += 1
                        exited += 1
                    else:
                        self.z[i] -= 2
                        self.z[i+1] += 1
                        self.z[i-1] += 1
                        # Add grain to next site
                        self.pile[i+1] += 1

                    # Choose new threshold slope value
                    self.z_th[i] = self.thold_gen(self.p)

                else:
                    noRelax += 1
            
                if noRelax == self.L - 1:
                    # Exit loop if a complete pass through all sites has
                    # been made without a relaxation.
                    completePass = True
        self.exitArray.append(exited)
        self.dataLog.add(self.pile, self.z, self.z_th, avalSize)

    def addGrain(self):
        self.drive()
        self.relax()
        return  None

    def steadyStateCheck(self, count):
        """
        Checks ratio of outgoing grains to input grains. If ratio is ~1,
        then system is in steady state.
        """
        if self.N < count:
            return False
        else:
            grainsOut = np.mean(self.exitArray[-count:])
            precision = 0.98    # Approx steady state threshold value (1 in -> 1 out)
            if grainsOut >= precision:  
                return True
            else:
                return False

    def returnPile(self):
        """
        Returns the array of heights for each site in the 
        pile. Can be plotted using a bar chart to visually 
        show the pile height.
        """
        return self.pile
    def plotPile(self):
        """
        Generates a bar plot of the current state of the pile. When Oslo object
        instantiated with a steadystatecheck, this becomes equivalent to 
        Datalog.plotSnapshot(-1), unless it is used before steady state reached.
        """
        L_axis = [i for i in range(0, self.L)]
        plt.bar(L_axis, self.returnPile(), width = 1, align = 'edge')
        plt.show()
        return (L_axis, self.returnPile())

    def returnGrad(self):
        """
        Return array of pile gradients for every site.

        # SHOULD BE ACCESSED FROM DATALOG OBJECT #
        """
        return self.z
    def returnThold(self):
        """
        Returns the threshold gradient for every site.

        # SHOULD BE ACCESSED FROM DATALOG OBJECT #
        """
        return self.z_th
    def returnExited(self, count):
        """
        Returns the array of grains exiting the system after
        each relaxation.
        """
        return self.exitArray[-count:]
    def returnLog(self):
        """
        Return the dataLog object of the pile.
        """
        return self.dataLog

def execute_piles(n, L):
    p = 0.5             # Oslo model probability parameter. Can be modified for investigation.
    full_entry = []
    for i in range(n):
        pile = Oslo(L, p)   # Instantiate pile
        ss = pile.steadyStateCheck(500)
        ss_runs = 3000
        j = 0
        while ss == False:
            # Drive pile until steady steate reached
            pile.addGrain()
            ss = pile.steadyStateCheck(500)
        while j < ss_runs:
            # After steady state reached, keep driving pile for fixed number
            # of runs. This keeps the standard deviations on the steady state
            # heights comparable.
            pile.addGrain()
            j += 1
        run_entry = {'Log' : pile.returnLog(), 'Size' : L, 'Run' : i}
        full_entry.append(run_entry)

    n = 1
    file_path = f'pickle/Oslo_{L}_{n}.npy'
    while os.path.exists(file_path):
        n += 1
        file_path = f'pickle/Oslo_{L}_{n}.npy'

    with open(file_path, 'wb') as file:
        np.save(file, full_entry)
    return file_path
        
def execute_all_sizes(n):
    for i in range(2, 9):
        L = 2**i
        execute_piles(n, L)

