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
        Simulates relaxation.
        """
        completePass = False

        while completePass == False:
            # for _z in self.z:
            #     i = self.z.where(_z)
            #     if i == self.L and _z > self.z_th[i]:
            #         self.z[i] -= 1
            #         self.z[i-1] += 1
            #     elif i == 0 and _z > self.z_th[i]:
            #         self.z[i] -= 2
            #         self.z[i+1] += 1
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
