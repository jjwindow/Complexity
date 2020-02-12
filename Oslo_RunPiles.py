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

# execute_10_piles(4)
# execute_10_piles(8)
# execute_10_piles(16)
# execute_10_piles(32)
# execute_10_piles(64)
# execute_10_piles(128)
# execute_10_piles(256)

execute_piles(3, 128)
execute_piles(3, 256)
# execute_all_sizes()