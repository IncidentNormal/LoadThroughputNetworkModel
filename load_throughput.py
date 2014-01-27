from SimPy.Simulation import *
import pylab as pyl
import numpy as np
import random
import math


class G():
    MEAN_TIME_BETWEEN_REQUEST = 2.
    MEAN_TIME_HOLD_CHANNEL = 0.1
    MEAN_BACKOFF = 0.1
    NUM_DEVICE = 0
    NUM_CHAN = 1
    MAX_TIME = 500

    endSeries = []
    end2Series = []
    ySeries = np.zeros(100)
    y2Series = np.zeros(100)
    LossCount = 0
    ThroughCount = 0

class Cont():
    CSMA = Resource(capacity=G.NUM_CHAN)
    Channel = Resource(capacity=G.NUM_CHAN)
    DeviceList = []

class Device(Process):
    def __init__(self,ID):
        Process.__init__(self)
        self.ID = ID
    def execute(self):
        yield hold,self,random.expovariate(1/G.MEAN_TIME_BETWEEN_REQUEST)
        while True:
            #print self.ID, 'CHECK csma len: ', len(Cont.CSMA.activeQ), 'chan len: ', len(Cont.Channel.activeQ)
            if (not len(Cont.CSMA.activeQ)==G.NUM_CHAN) and (not (Cont.Channel.activeQ)==G.NUM_CHAN):
                #print self.ID, 'REQ csma len: ', len(Cont.CSMA.activeQ), 'chan len: ', len(Cont.Channel.activeQ)
                yield request,self,Cont.CSMA
                yield hold,self,0.01
                if self.interrupted():
                    G.LossCount += 1
                    yield release,self,Cont.CSMA
                    #print self.ID, 'was interrupted! -- Collision occured'
                    #G.Count += 1
                    yield hold,self,random.expovariate(1/G.MEAN_BACKOFF)
                else:
                    #print self.ID, 'no collision, through'
                    #print G.ThroughCount
                    G.ThroughCount += 1
                    yield release,self,Cont.CSMA
                    #print self.ID, 'csma len: ', len(Cont.CSMA.activeQ), 'REQ chan len: ', len(Cont.Channel.activeQ)
                    yield request,self,Cont.Channel
                    yield hold,self,random.expovariate(1/G.MEAN_TIME_HOLD_CHANNEL)
                    yield release,self,Cont.Channel
                    yield hold,self,random.expovariate(1/G.MEAN_TIME_BETWEEN_REQUEST)
                    
            elif (len(Cont.CSMA.activeQ)==G.NUM_CHAN) and (not (Cont.Channel.activeQ)==G.NUM_CHAN):
                for D in Cont.CSMA.activeQ:
                    #print self.ID, 'is interrupting!'
                    self.interrupt(D)
                    yield hold,self,random.expovariate(1/G.MEAN_BACKOFF)

for run in range(1000):
    print 'run', run
    for load in range(2,100):
        G.NUM_DEVICE=load
        initialize()
        for i in range(G.NUM_DEVICE):
            D = Device(i)
            Cont.DeviceList.append(D)
            activate(Cont.DeviceList[i],Cont.DeviceList[i].execute(),at=0.0)
        simulate(until=G.MAX_TIME)
        print load, G.ThroughCount, G.LossCount
        G.ySeries[load] += G.ThroughCount
        G.y2Series[load] += G.LossCount
        G.ThroughCount = 0
        G.LossCount = 0
        Cont.CSMA = Resource(capacity=G.NUM_CHAN)
        Cont.Channel = Resource(capacity=G.NUM_CHAN)
        Cont.DeviceList = []

print 'end of Run, start Vis'

for load in G.ySeries:
    G.endSeries.append(load/4000.)
for load in G.y2Series:
    G.end2Series.append(load/4000.)

pyl.subplot(2, 1, 1)
pyl.plot(range(100),G.endSeries)
pyl.title('Throughput and Loss as a function of Number of Nodes')
pyl.ylabel('Throughput')
pyl.subplot(2, 1, 2)
pyl.plot(range(100),G.end2Series)
pyl.ylabel('Loss')
pyl.xlabel('Num Nodes')
pyl.show()

        
