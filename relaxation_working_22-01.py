<<<<<<< HEAD
"""
First attempt at implementation of the Oslo model, 22/1/2020
-Alternative using OOP
J. J. Window
"""
import numpy as np
from random import choice
from random import random
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
        self.heightsLog.append(newHeights)
        self.gradsLog.append(newGrads)
        self.tholdsLog.append(newTholds)

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

        self.L = L
        self.p = p
        self.exited = 0
        self.dataLog = Datalog(self.L, self.p)

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
                        self.exited += 1
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
            
            if noRelax == self.L:
                # Exit loop if a complete pass through all sites has
                # been made without a relaxation.
                completePass = True
                self.dataLog.add(self.pile, self.z, self.z_th)


    def returnpile(self):
        return self.pile
    def returngrad(self):
        return self.z
    def returnthold(self):
        return self.z_th
    def returnexited(self):
        return self.exited
    def returnLog(self):
        return self.dataLog


### TO DO ###
#   - Figure out animations
#   - Define func in Datalog that animates using elements in heights.

L = 64
p=0.5
pile = Oslo(L, p)
a = 0
while a < 2000:
    a += 1
    pile.drive()
    pile.relax()

pileLog = pile.returnLog()
(h, z, z_th) = pileLog.getSnapshot(1999)

L_axis = [i for i in range(0, L)]
plt.bar(L_axis, pile.returnpile(), width = 1, align = 'edge')
plt.show()
plt.bar(L_axis, h, width = 1, align = 'edge')
plt.show()
print(pile.returnpile())
print(pile.returngrad())
print(pile.returnthold())
print(pile.returnexited())
=======
"""
First attempt at implementation of the Oslo model, 22/1/2020
-Alternative using OOP
J. J. Window
"""
import numpy as np
from random import choice
from random import random

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

        self.L = L
        self.p = p
        self.exited = 0

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
                        self.exited += 1
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
            
            if noRelax == self.L:
                # Exit loop if a complete pass through all sites has
                # been made without a relaxation.
                completePass = True


    def returnpile(self):
        return self.pile
    def returngrad(self):
        return self.z
    def returnthold(self):
        return self.z_th
    def returnexited(self):
        return self.exited

pile = Oslo(5, 0.5)
a = 0
while a < 50:
    a += 1
    pile.drive()
    pile.relax()
print(pile.returnpile())
print(pile.returngrad())
print(pile.returnthold())
print(pile.returnexited())
>>>>>>> bda613ad14ae9273a215215c84eca36a36b6ffd4
