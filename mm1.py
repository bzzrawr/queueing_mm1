import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import heapq as hq
import numpy as np

class simulation(object):
    def __init__(self,maxque,iat):
        '''initialize all the simulation value'''
        self.meanarrivalrate = iat
        self.meanservicerate = 10
        self.simclock = 0.0     #simulation clock
        self.at = self.pg()
        self.dt = float('inf')  #packet departure time
        self.et = 0.0           #event time
        self.sink = []          #current packet in the server
        self.n_arrival = 0      #no of packet arrival
        self.n_depart = 0       #no of packet departure
        self.npdrop = 0         #no of packet drop
        self.id = 0             #packet id
        self.status = 'idle'    #server status
        self.cqs = 0            #current queue size
        self.maxque = maxque
        self.tmpd = 0.0         #temp value for calculating delay
        self.t2 = None          #temp value for calculating delay
        self.plr = 0.0          #packet loss rate
        self.npdelay = 1        #no of packet delayed
        self.arrival = 'arrive'        #
        self.departure = 'depart'
        self.evt = Event()
        self.Queue = Queue(self.maxque,self.evt)
        self.Ser_ver = Server()
        self.totalbusy = 0.0
        self.prevEvent = 0.0
        self.avgQ = 0.0
        self.meanSW = 0.0
        self.result = calc_result()
        self.meanQW = 0.0
        self.meanSW = 0.0
        self.meanQ = 0.0
        self.meanS = 0.0
        self.rho = 0.0

#========================================================================
#   scheduling an event and update simulation clock
#========================================================================
    def scheduling(self):
        self.et = min(self.at,self.dt)
        if self.at <= self.dt:
            self.evt.Event(self.arrival,self.et)
        else:
            self.evt.Event(self.departure,self.et)

    def uclock(self):
        self.simclock = self.evt.getTime()

    def etype(self):
        if self.evt.getType() == 'arrive':
            self.processArrival()
        else:
            self.processDeparture()

#========================================================================
#   function to schedule next packet arrival and departure
#========================================================================
    def processArrival(self):
        self.n_arrival +=1
        cqs = len(self.Queue.cQ())
        if cqs < self.maxque:
            self.Queue.enQ(self.evt.getTime())

            if self.Ser_ver.checkServer() == 'idle':
                tmpd = self.Queue.deQ()
                self.Ser_ver.inServer(tmpd)
                if cqs <=1:
                    st1 = self.sg()
                    self.dt = self.simclock + st1
            else:
                self.totalbusy+=(self.simclock - self.prevEvent)
        else:
            self.npdrop+=1
        self.at = self.simclock + self.pg()
        self.avgQ += ((self.simclock - self.prevEvent)*cqs)
        self.meanSW += (((self.simclock - self.prevEvent)*cqs)+(self.dt-self.simclock))
        self.prevEvent = self.simclock

    def processDeparture(self):
        self.n_depart +=1
        self.npdelay +=1
        cqs = len(self.Queue.cQ())
        self.totalbusy +=(self.simclock - self.prevEvent)
        self.avgQ += ((self.simclock - self.prevEvent)*cqs)
        self.meanSW += (((self.simclock - self.prevEvent)*cqs)+(self.dt-self.simclock))
        self.prevEvent = self.simclock
        self.Ser_ver.outServer()
        if cqs > 0:
            tmpd = self.Queue.deQ()
            self.Ser_ver.inServer(tmpd)
            st2 = self.sg()
            self.dt = self.simclock + st2
        else:
            self.dt = float('inf')

#========================================================================
#   function to generate result report
#========================================================================
    def reportGeneration(self):
        self.rho = self.result._rho(self.totalbusy,self.simclock)
        self.meanS = self.result._meanSW(self.meanSW,self.simclock)
        self.meanQ = self.result._avgQ(self.avgQ,self.simclock)
        self.meanSW = self.meanS/self.meanarrivalrate
        self.meanQW = self.meanQ/self.meanarrivalrate
        self.plr = self.result._plr(self.npdrop,self.n_arrival)

#========================================================================
#   function to generate packet and service
#========================================================================
    def pg(self):
        return np.random.exponential(1/self.meanarrivalrate)
        
    def sg(self):
        return np.random.exponential(1/self.meanservicerate)


#========================================================================
#   class to store event, packet in queue and packet in server
#========================================================================
class Event(object):
    def __init__(self):
        self._time = None
        self._type = None
    def Event(self, eType, time):
        self._type = eType
        self._time = time

    def getType(self):
        return self._type

    def getTime(self):
        return self._time

class Queue:
    def __init__(self,maxQ,evt):
        self._que = []
        self.maxQ = maxQ
        self.evt = evt

    def enQ(self,packet):
        hq.heappush(self._que,packet)

    def deQ(self):
        return hq.heappop(self._que)

    def getFront(self):
        return self._que[0]
    def cQ(self):
        return self._que

class Server:
    def __init__(self):
        self._sink = []
        self.status = None

    def inServer(self,packet):
        self._sink.append(packet)

    def outServer(self):
        self._sink.pop(0)

    def checkServer(self):
        if len(self._sink) == 0:
            self.status = 'idle'
        else:
            self.status = 'busy'

        return self.status

#========================================================================
#   class to calculate result
#========================================================================

class calc_result:
    def __init__(self):
        self.rho = 0.0
        self.meanQWelay = 0.0
        self.avgQ = 0.0
        self.meanSW = 0.0
        self.plr = 0.0

    def _rho(self,totalbusy,simclock):
        self.rho = totalbusy/simclock
        return self.rho

    def _avgQ(self,avgQ,simclock):
        self.avgQ = avgQ/simclock
        return self.avgQ

    def _meanSW(self,meanSW,simclock):
        self.meanSW = meanSW/simclock
        return self.meanSW

    def _plr(self,npdrop,n_arrival):
        self.plr = npdrop/n_arrival
        return self.plr
#========================================================================
#   class to plot graph
#========================================================================
class plot_graph:
    def __init__(self):
        self.index = np.arange(100)
        self.fig1, (self.df1,self.df2) = plt.subplots(2)
        # self.fig2, self.df2 = plt.subplots()
    def average_delay(self,data):
        self.df1.plot(self.index,data,color='red', label='Wq')
        self.df1.set_ylabel('TIME (s)', fontsize=7)
        self.df1.set_xlabel('MEAN RATE OF ARRIVAL (λ)', fontsize=7)
        self.df1.legend()
        self.df1.set_title('AVERAGE WAITING TIME IN THE SYSTEM (Ws) VS AVERAGE WAITING TIME IN THE QUEUE (Wq)',fontsize=7)
        
    def average_system(self,data):
        self.df1.plot(self.index,data,color='green', label='Ws')
        
    def average_packetS(self,data):
        self.df2.plot(self.index,data,color='yellow', label='Ls')
        self.df2.set_xlabel('MEAN RATE OF ARRIVAL (λ)', fontsize=7)
        self.df2.set_ylabel('TIME (s)', fontsize=7)
        self.df2.legend()
        self.df2.set_title('AVERAGE PACKET IN THE SYSTEM (Ls) VS AVERAGE PACKET IN THE QUEUE (Lq)',fontsize=7)

    def average_packetQ(self,data):
        self.df2.plot(self.index, data,color='blue', label='Lq')
        self.df2.legend()

    def cpu_util(self,data):
        fig5, df5 = plt.subplots()
        df5.plot(self.index,data,color='cyan')
        df5.set_xlabel('MEAN RATE OF ARRIVAL(λ)')
        df5.set_ylabel('TRAFFIC INTENSITY (ρ)')

    def packet_loss_ratio(self,data):
        fig6, df6 = plt.subplots()
        df6.plot(self.index,data,color='magenta')
        df6.set_xlabel('MEAN RATE OF ARRIVAL(λ)')
        df6.set_ylabel('PACKET LOSS RATIO')    

        return plt.show()

#========================================================================
#   main program that will run the simulation accordingly
#========================================================================        
if __name__ == "__main__":
    b = plot_graph()
    meanQW = []                 #   store value for average waiting time in the queue
    meanSW = []                 #   store value for average waitint time in the system
    meanQ = []                  #   store value for average packet in queue
    meanS = []                  #   store value for average packet in the system
    traffic_intensity = []      #   store value for traffic intensity
    plr = []                    #   store value for packet loss ratio

    for runSim in range(1,101): #load (λ) iteration
        a = simulation(10,runSim)
        totalpacket = 50000     #total packet sent
        x = totalpacket * 2
        np.random.seed(0)
        for i in range(x):
            a.scheduling()
            a.uclock()
            a.etype()
        a.reportGeneration()
        meanQW.append(a.meanQW)
        meanSW.append(a.meanSW)
        meanQ.append(a.meanQ)
        meanS.append(a.meanS)
        traffic_intensity.append(a.rho)
        plr.append(a.plr)

    b.average_packetS(meanS)
    b.average_packetQ(meanQ)
    b.average_system(meanSW)
    b.average_delay(meanQW)
    b.cpu_util(traffic_intensity)
    b.packet_loss_ratio(plr)
    
    
