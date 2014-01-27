'''
Created on Jul 14, 2010

@author: duncantait
'''
from SimPy.Simulation import *
import random
import math

class G():
    MEAN_TIME_BETWEEN_MESSAGES = 10
    NETWORK_LOAD = 0
    MAX_SYSTEM_LOAD = 100
    PERCENT_DETERIORATION = 50
    PERCENT_LOSS_RATE = 0
    
    
class Load(Process):
    def __init__(self):
        Process.__init__(self)
        self.currentLoad = 0
    def execute(self):
        while True:
            self.currentLoad = abs(3*math.sin(now())) + random.uniform(0,3)
            G.NETWORK_LOAD = self.currentLoad
            G.PERCENT_LOSS_RATE = 
            yield hold,self,0.01
    def calc_loss(self):
        
        




initialize()
L = Load()
activate(L,L.execute(),at=0.0)
simulate(until=10.0)