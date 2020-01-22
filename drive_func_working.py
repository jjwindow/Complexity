"""
First attempt at implementation of the Oslo model, 22/1/2020
-Alternative using OOP
J. J. Window
"""
import numpy as np
from random import choice
from random import random

class Oslo:

    def __init__(self, L, p):

        # Check arguments are valid
        L = int(L)
        if type(p) is not float:
            raise TypeError("Argument p must be of type float")
        if (p<0) or (p>1):
            raise Exception("Argument p must be a valid probability 0 <= p <= 1")

        self.L = L
        self.p = p
        self.thold_vals = [1,2]

        # Initialise pile with empty sites
        self.pile = np.zeros(L) 
        # Define gradients from i = 0 to L-1
        self.z = [i-j for i, j in zip(self.pile, self.pile[1:])]
        # Add i=L gradient (0 at initialisation)
        self.z.append(0)
            
        def thold_gen(self):
            """
            Generates a new threshold value for a given site. Can be called at
            initialisation or relaxation. Parameter p is the probability a site
            gets a threshold value of 1. A threshold value of 2 has an associated 
            probability of (1-p).
            """
            # # Pick between [1, 2] with equal probability
            # if self.p == 0.5:
            #     z_th = choice(self.thold_vals)
            # # For general p != 0.5:
            # randnum = random()
            # if randnum <= self.p:
            #     z_th = self.thold_vals[0]
            # else:
            #     z_th = self.thold_vals[1]

            z_th = np.random.choice(self.thold_vals, p = [self.p, 1-self.p])
            return z_th

        self.z_th = [thold_gen(self) for _ in range(0, self.L)]

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
        relax = True

        while relax:
            for _z in self.z:
                i = self.z.where(_z)
                if i == 1 and _z > z_th[i]:
                    self.z[i] -= 2


    def returnpile(self):
        return self.pile
    def returngrad(self):
        return self.z
    def returnthold(self):
        return self.z_th

pile = Oslo(5, 0.5)
print(pile.returnpile())
print(pile.returngrad())
print(pile.returnthold())
pile.drive()
print(pile.returnpile())
print(pile.returngrad())
print(pile.returnthold())