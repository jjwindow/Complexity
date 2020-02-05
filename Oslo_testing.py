"""
J. J. Window
Complexity Project, Complexity & Networks
3rd Year MSci Physics
Imperial College London

Implementation and testing of the Oslo Model module Oslo.py.
"""
from Oslo import *

###     SYSTEM PARAMS     ###

L = 64             # Define system Size
p=0.5               # Probability that a new threshold will
                    # have value = 1.
pile = Oslo(L, p)   # Instantiate pile object

###     PILE TESTING       ###

r = pile.steadyStateCheck(1000)
while r == False:
    # Drive pile until steady steate reached
    pile.addGrain()
    r = pile.steadyStateCheck(1000)

pileLog = pile.returnLog()      # Retrieve pile history
pile.plotPile()                 # Plot final pile

# Average height during steady state
print(pileLog.getHeightAvg(250))  





