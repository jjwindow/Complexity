"""
J. J. Window
Complexity Project, Complexity & Networks
3rd Year MSci Physics
Imperial College London

Oslo Model script to bulk simulate the sandpiles of sizes:
L = 4, 8, 16, 32, 64, 128, 256

Resulting piles have their attributes stored in their Datalog classes,
which are stored as .pkl files in the /pickle directory.

Each pile size is run 10 times, generating 10 objects for each length
=> total = 70 pile objects.

These objects are interrogated in other scripts.
"""

from Oslo import *
import numpy as np
from pickle import dump, load

#execute_piles(10, 4)

execute_all_sizes(5)