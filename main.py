from random import random

from  simulationMM2 import run_sim_mm2
from  simulationMM1 import run_sim_mm1

"""
 Run Simulation Here :D  
"""

run_sim_mm1()
#run_sim_mm2()








def choi_de_guichet(probability):
    r = random()
    print('probs', probability)
    print('r', r)
    if r < 1 - probability:
        print('hi')
    else:
        print('no')
#choi_de_guichet(1/3)
''''
def mygen(n):
    for i in range(n):
        yield i*i


a=mygen(10)
print(a)
print(next(a))
'''