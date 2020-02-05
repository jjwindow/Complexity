"""
J. J. Window
Complexity Project, Complexity & Networks
3rd Year MSci Physics
Imperial College London

Implementation and testing of the Oslo Model module Oslo.py.
"""

L = 32
p=0.5
pile = Oslo(L, p)
a = 0
r = pile.steadyStateCheck(1000)
while r == False:
    pile.addGrain()
    r = pile.steadyStateCheck(1000)

pileLog = pile.returnLog()
h, z, z_th = pileLog.getSnapshot(-1)
print(pileLog.getHeightAvg(250))
L_axis = [i for i in range(0, L)]
plt.bar(L_axis, pile.returnpile(), width = 1, align = 'edge')
plt.show()

j = 0
while j < 5:
    pile.drive()
    pile.relax()
    plt.bar(L_axis, pile.returnpile(), width = 1, align = 'edge')
    j += 1
pileLog = pile.returnLog()



