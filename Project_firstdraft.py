"""
First attempt at implementation of the Oslo model, 22/1/2020
J. J. Window
"""

import scipy as sp
from random import random

def Oslo(L, p):
    """ 
    Oslo model of ricepile problem. Takes parameters L as size of system
    and p as probability of new threshold being chosen as z=1.
    """
    # Initialise pile array with h = 0 in every site.
    pile = sp.zeros(L)

    def thold_gen(p):
        """
        Generates a new threshold value for a given site. Can be called at
        initialisation or relaxation. Parameter p is the probability a site
        gets a threshold value of 1. A threshold value of 2 has an associated 
        probability of (1-p).
        """
        print(type(p))
        # Check p is a valid probability
        if type(p) is not float:
            raise TypeError("Argument p must be a float number")
        if (p<0) or (p>1):
            raise Exception("Argument p must be between 0 and 1 since it is a probability.")

        # Select threshold value
        randnum = random()
        if randnum <= p:
            z_th = 1
        else:
            z_th = 2

        return z_th

    # Generate array of threshold values for sites.
    thold = [thold_gen(p) for i in range(0, L)]

    print(pile)
    print(thold)

Oslo(5, 0.5)

    
