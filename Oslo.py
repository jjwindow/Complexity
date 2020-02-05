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
        self.heightsLog = []
        self.gradsLog = []
        self.tholdsLog = []

    def add(self, newHeights, newGrads, newTholds):
        """
        Adds new data to class attributes.
        """
        self.heightsLog.append(copy.copy(newHeights))
        self.gradsLog.append(copy.copy(newGrads))
        self.tholdsLog.append(copy.copy(newTholds))

    def getSnapshot(self, n):
        """
        Returns the nth instance of the datalog - i.e, a snapshot of the pile after drive n.
        """

        if type(n) is not int:
            raise TypeError("n parameter must be an integer.")
        return (self.heightsLog[n],self.gradsLog[n],self.tholdsLog[n])
    
    def getFullHist(self):
        """
        Returns all class attributes in full.
        """
        return (self.heightsLog, self.gradsLog, self.tholdsLog)

    def getNumGrains(self, n):
        """
        Returns number of grains in the system at any one time.
        """
        return sum(self.heightsLog[n])

    def getHeightAvg(self, n):
        """
        Returns average pile height for n most recent drives.
        """
        return np.mean([self.heightsLog[-i][0] for i in range(0, n)])



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
        self.dataLog.add(self.pile, self.z, self.z_th)

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
            grainsOut = sum(self.exitArray[-count:])
            r = grainsOut/count
            precision = 0.9    # Approx steady state threshold value 
            if r >= precision:  
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
        L_axis = [i for i in range(0, self.L)]
        plt.bar(L_axis, self.returnPile(), width = 1, align = 'edge')
        plt.show()
        return (L_axis, self.returnPile())
    def returnGrad(self):
        """
        Return array of pile gradients for every site.
        """
        return self.z
    def returnThold(self):
        """
        Returns the threshold gradient for every site.
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
