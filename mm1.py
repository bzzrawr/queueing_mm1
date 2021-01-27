import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import heapq as hq
import numpy as np

class simulation(object):
    def __init__(self,maxque):
        '''initialize all the simulation value'''
        self.meanarrivalrate = int(input("Insert arrival rate: "))
        self.meanservicerate = int(input("Insert service rate: "))
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
        # self.maxque = 99999999
        self.maxque = maxque
        self.tdelay = 0.0       #total delay
        self.inq = []           #packet in the queue
        self.tmpd = 0.0         #temp value for calculating delay
        self.t2 = None          #temp value for calculating delay
        self.avgdelay = 0       #average delay
        self.plr = 0.0          #packet loss rate
        self.npdelay = 1        #no of packet delayed
        self.arrival = 'arrive'        #
        self.departure = 'depart'
        self.evt = Event()
        self.Queue = Queue(self.maxque,self.evt)
        self.Ser_ver = Server()
        self.totalbusy = 0.0
        self.prevEvent = 0.0
        self.sumResponse = 0.0
        self.avgQ = 0.0
        self.avgS = 0.0
        self.result = calc_result()
        self.iDle = 0.0
        self.nPidle = 0
        self.p10 = 0.0
        self.nP10 = 0
        self.nPnQ = 0
        self.noQ = 0.0
        self.graph1 = []
        self.graph2 = []

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
        self.avgS += (((self.simclock - self.prevEvent)*cqs)+(self.dt-self.simclock))
        self.prevEvent = self.simclock

    def processDeparture(self):
        self.n_depart +=1
        self.npdelay +=1
        cqs = len(self.Queue.cQ())
        self.totalbusy +=(self.simclock - self.prevEvent)
        self.avgQ += ((self.simclock - self.prevEvent)*cqs)
        self.avgS += (((self.simclock - self.prevEvent)*cqs)+(self.dt-self.simclock))
        self.prevEvent = self.simclock
        self.Ser_ver.outServer()
        if cqs > 0:
            tmpd = self.Queue.deQ()
            self.calc_delay(self.dt,tmpd)
            self.Ser_ver.inServer(tmpd)
            st2 = self.sg()
            self.dt = self.simclock + st2
        else:
            self.dt = float('inf')

#========================================================================
#   function to generate result report
#========================================================================
    def reportGeneration(self):
        rho = self.result._rho(self.totalbusy,self.simclock)
        meanS = self.result._avgS(self.avgS,self.simclock)
        meanQ = self.result._avgQ(self.avgQ,self.simclock)
        meanSW = meanS/self.meanarrivalrate
        meanQW = meanQ/self.meanarrivalrate
        self.graph1 = [rho,self.iDle,self.noQ,self.p10]
        self.graph2 = [meanS,meanQ,meanSW,meanQW]
        print("======================================")
        print("SINGLE SERVER QUEUE SIMULATION REPORT")
        print("======================================")
        print("MEAN INTERARRIVAL TIME: ",self.meanarrivalrate)
        print("MEAN SERVICE TIME: ",self.meanservicerate)
        print("SIMULATION RUNLENGTH: ",self.simclock)
        print("NUMBER OF PACKET ARRIVAL: ", self.n_arrival)
        print("NUMBER OF PACKET DEPARTURE: ", self.n_depart)
        print("SERVER UTILIZATION: ", rho)
        print("PROBABILITY OF IDLE: ", self.iDle)
        print("PROBABILITY OF NO QUEUE: ",self.noQ)
        print("PROBABILITY OF 10 PACKET IN SYSTEM: ", self.p10)
        print("MEAN NUMBER OF PACKET IN THE SYSTEM: ",meanS)
        print("MEAN NUMBER OF PACKET IN THE QUEUE: ",meanQ)
        print("MEAN WAITING TIME IN THE SYSTEM: ",meanSW)
        print("MEAN WAITING TIME IN THE QUEUE: ",meanQW)
        print(self.graph1)
        print(self.graph2)

    def calc_delay(self,depT,arrT):
        self.tdelay += (depT - arrT)

    def cal_prob(self):
        if len(self.Queue.cQ()) == 0 and len(self.Ser_ver._sink) == 0:
            self.nPidle +=1
            self.iDle = self.nPidle/self.n_arrival

        if len(self.Queue.cQ()) == 0 and len(self.Ser_ver._sink) == 1:
            self.nPnQ +=1
            self.noQ = self.nPnQ/self.n_arrival

        if len(self.Queue.cQ()) == 9 and len(self.Ser_ver._sink) == 1:
            self.nP10 +=1
            self.p10 = self.nP10/self.n_arrival

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
        self.avgdelay = 0.0
        self.avgQ = 0.0
        self.avgS = 0.0
        self.plr = 0.0

    def _rho(self,totalbusy,simclock):
        self.rho = totalbusy/simclock
        return self.rho

    def _avgdelay(self,tdelay,npdelay):
        self.avgdelay = tdelay/npdelay
        return self.avgdelay

    def _avgQ(self,avgQ,simclock):
        self.avgQ = avgQ/simclock
        return self.avgQ

    def _avgS(self,avgS,simclock):
        self.avgS = avgS/simclock
        return self.avgS

    def _plr(self,npdrop,n_arrival):
        self.plr = npdrop/n_arrival
        return self.plr
#========================================================================
#   class to plot graph
#========================================================================
class plot_graph:
    def __init__(self):
        self.index = np.arange(4)
        self.column1 = ['Traffic intensity','P0','No queue','P10']
        self.bar1 = None
        self.bar2 = None
        self.mm1inf = [0.89,0.11,0.20,0.03]
        self.mm1N = [0.89,0.15,0.28,0.05]

    # def var_param1(self,value1,value2):
    #     fig1, (df1,df2) = plt.subplots(2)
    #     df1.plot(self.column1,value1,marker="D",color='#18A700',label='Simulation')
    #     df1.set_ylabel('Probability')
    #     df1.set_title('M/M/1:∞/∞')
    #     df1.plot(self.column1, self.mm1inf,marker="D",color='#FF0000',label='Calculation')
    #     df2.plot(self.column1,value2,marker="D",color='#22EC00',label='Simulation')
    #     df2.set_ylabel('Probability')
    #     df2.set_title('M/M/1:N/∞')
    #     plt.legend()
    def var_param1_1(self,value):
        fig1, ax = plt.subplots()
        ax.plot(self.column1,value,marker="D",color='#18A700',label='Simulation')
        ax.plot(self.column1, self.mm1inf,marker="D",color='#FF0000',label='Calculation')
        ax.set_ylabel('Probability')
        ax.set_title('M/M/1:∞/∞')
        plt.legend()

    def var_param1_2(self,value):
        fig2, ax = plt.subplots()
        ax.plot(self.column1,value,marker="D",color='#22EC00',label='Simulation')
        ax.plot(self.column1, self.mm1N,marker="D",color='#FF0000',label='Calculation')
        ax.set_ylabel('Probability')
        ax.set_title('M/M/1:N/∞')
        plt.legend()

    def var_param2(self,value1,value2):
        fig3, ax = plt.subplots()
        x = np.array([1,2,3,4])
        xnew = np.linspace(x.min(),x.max(),150)

        y1 = np.array(value1)
        y2 = np.array(value2)

        sp1 = make_interp_spline(x,y1,k=2)
        sp2 = make_interp_spline(x,y2,k=3)
        y_smooth1 = sp1(xnew)
        y_smooth2 = sp2(xnew)
        plt.plot(xnew, y_smooth1, linestyle='-',color='green',label='M/M/1:∞/∞')
        plt.plot(x,y1, 'o', color='green')
        plt.plot(xnew, y_smooth2, linestyle='-',color='red',label = 'M/M/1:N/∞')
        plt.plot(x,y2, 'o', color='red')
        plt.xticks(self.index+1,('Ls','Lq','Ws','Wq'))
        plt.ylabel('Probability')
        plt.title('Probability of various parameters Ls, Lq, Ws & Wq')
        plt.legend()
        

    def bar_chart_1(self,value1,value2):
        fig4, ax = plt.subplots()
        self.bar1 = value1
        self.bar2 = value2
        bar_width = 0.35
        opacity = 0.8

        rects1 = plt.bar(self.index, self.bar1,bar_width, alpha=opacity, color='green', label = 'M/M/1:∞/∞')
        rects2 = plt.bar(self.index+bar_width, self.bar2, bar_width, alpha = opacity, color='red', label = 'M/M/1:N/∞')
        plt.ylabel('Probability')
        plt.title('Comparison Between Queuing Model (Simulation)')
        plt.xticks(self.index + bar_width,('Traffic intensity','P0','No queue','P10'))
        plt.legend()

    def bar_chart_2(self):
        fig5, ax = plt.subplots()
        bar_width = 0.35
        opacity = 0.8

        rects1 = plt.bar(self.index, self.mm1inf,bar_width, alpha=opacity, color='#22EC00', label = 'M/M/1:∞/∞')
        rects2 = plt.bar(self.index+bar_width, self.mm1N, bar_width, alpha = opacity, color='#FF3399', label = 'M/M/1:N/∞')
        plt.ylabel('Probability')
        plt.title('Comparison Between Queuing Model (Calculation)')
        plt.xticks(self.index + bar_width,('Traffic intensity','P0','No queue','P10'))
        plt.legend()
        return plt.show()


#========================================================================
#   main program that will run the simulation accordingly
#========================================================================        
if __name__ == "__main__":
    b = plot_graph()
    typ = []
    for runSim in range(2):
        while True:
            try:
                maxque = float(input("Enter maximum queue size: "))
                break
            except ValueError:
                print("Enter valid number!")

        a = simulation(maxque)
        x = 99999
        # x = 13
        np.random.seed(0)
        if maxque == float('inf'):
            for i in range(x):
                a.scheduling()
                a.uclock()
                a.etype()
                a.cal_prob()
            a.reportGeneration()
            typ.append(a.graph1)
            typ.append(a.graph2)
        else:
            for i in range(x):
                a.scheduling()
                a.uclock()
                a.etype()
                a.cal_prob()
            a.reportGeneration()
            typ.append(a.graph1)
            typ.append(a.graph2)
    b.var_param1_1(typ[0])
    b.var_param1_2(typ[2])
    b.var_param2(typ[1],typ[3])
    b.bar_chart_1(typ[0],typ[2])
    b.bar_chart_2()    
    
