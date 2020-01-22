"""
First attempt at implementation of the Oslo model, 22/1/2020
-Alternative using OOP
J. J. Window
"""
import numpy as np
from random import choice
from random import random

class Oslo:
    thold_vals = [1,2]
    def __init__(self, L, p):

        # Check arguments are valid
        L = int(L)
        if type(p) is not float:
            raise TypeError("Argument p must be of type float")
        if (p<0) or (p>1):
            raise Exception("Argument p must be a valid probability 0 <= p <= 1")

        self.L = L
        self.p = p

        # Initialise pile with empty sites
        self.pile = np.zeros(L) 
        # Define gradients
        self.z = [i-j for i, j in zip(pile, pile[1:])]
            
        def thold_gen(self):
                """
                Generates a new threshold value for a given site. Can be called at
                initialisation or relaxation. Parameter p is the probability a site
                gets a threshold value of 1. A threshold value of 2 has an associated 
                probability of (1-p).
                """
                # Pick between [1, 2] with equal probability
                if self.p == 0.5:
                    z_th = choice(thold_vals)
                # For general p != 0.5:
                randnum = random()
                if randnum <= self.p:
                    z_th = 1
                else:
                    z_th = 2       
            return z_th

            self.z_th = [self.thold_gen() for _ in range(0, self.L)]


    def drive(self):
        """
        Adds a 'grain' to the leftmost site of the pile.
        """
        self.pile[0] += 1