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

allPiles = []

for i in range(2, 9):
    n = 2**i
    with open(f'Oslo_Investigation/Final_runs/Oslo_{n}.npy', 'rb') as file:
        allPiles.append(np.load(file, allow_pickle=True))

"""
allPiles is of form:

[ {'Pile' : pile_obj, 'size' = 4, ...}, 
  {..., 'size' = 8, ...              }  
   ...                      { = 256, } ]
"""

print(allPiles)

