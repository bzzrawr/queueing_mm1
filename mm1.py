import heapq as hq
import numpy as np

class simulation(object):
    def __init__(self):
        self.simclock = 0.0     #simulation clock
        # self.at = 0.4           #packet arrival time
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
        # self.maxque = int(input("Enter maximum que:")) #maximum queue size
        self.maxque = 10
        # self._iat = [1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9,0.8]
        # self._dpt = [2.0,0.7,0.2,1.1,3.7,0.6,float('inf')]
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
        self.QQ = fifo(self.maxque,self.evt)
        self.Ser_ver = Server()
        self.totalbusy = 0.0
        self.prevEvent = 0.0
        self.sumResponse = 0.0
        self.avgQ = 0.0
        self.avgS = 0.0

    def scheduling(self):
        self.et = min(self.at,self.dt)  #scheduling for event time
        if self.at <= self.dt:
            self.evt.Event(self.arrival,self.et)
        else:
            self.evt.Event(self.departure,self.et)
        # print("server status: ",self.status)
        # print("Currently in queue: ",len(self.QQ.cQ()))
        # print("Packet in server: ",self.Ser_ver._sink)
        # print("Packet in queue: ",self.QQ.cQ())
        # print("No of packet arrived: ",self.n_arrival)
        # print("No of packet departed: ",self.n_depart)
        # print("No of packet dropped: ",self.npdrop)
        # print("event time:",self.evt.getTime())
        # print("arrival time:",self.at,"departure time:",self.dt)
        # print("------------------------------------------------")


    def uclock(self):
        self.simclock = self.evt.getTime()

        

    def etype(self):
        if self.evt.getType() == 'arrive':
            self.processArrival()
        else:
            self.processDeparture()

    def processArrival(self):
        self.n_arrival +=1
        cqs = len(self.QQ.cQ())
        if cqs < self.maxque:
            self.QQ.enQ(self.evt.getTime())

            if self.Ser_ver.checkServer() == 'idle':
                x = self.QQ.deQ()
                self.Ser_ver.inServer(x)
                if cqs <=1:
                    st1 = self.sg()
                    # print(">>>>>Service time>>>",st1)
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
        cqs = len(self.QQ.cQ())
        finished = self.evt
        response = (self.simclock-finished.getTime())
        self.sumResponse +=response
        self.totalbusy +=(self.simclock - self.prevEvent)
        self.avgQ += ((self.simclock - self.prevEvent)*cqs)
        self.avgS += (((self.simclock - self.prevEvent)*cqs)+(self.dt-self.simclock))
        self.prevEvent = self.simclock
        self.Ser_ver.outServer()
        if cqs > 0:
            
            self.Ser_ver.inServer(self.QQ.deQ())
            st2 = self.sg()
            # print(">>>>Service time<<<<",st2)
            self.dt = self.simclock + st2
        else:
            self.dt = float('inf')

    def reportGeneration(self):
        rho = self.totalbusy/self.simclock
        avgr = self.sumResponse/self.n_arrival
        avgQ = self.avgQ/self.simclock
        avgS = self.avgS/self.simclock
        print("======================================")
        print("SINGLE SERVER QUEUE SIMULATION REPORT")
        print("======================================")
        # print("MEAN INTERARRIVAL TIME",self.)
        print("SIMULATION RUNLENGTH: ",self.simclock)
        print("NUMBER OF PACKET ARRIVAL: ", self.n_arrival)
        print("NUMBER OF PACKET DEPARTURE: ", self.n_depart)
        print("SERVER UTILIZATION: ", rho)
        print("AVERAGE RESPONSE TIME: ", avgr)
        print("AVERAGE NUMBER IN QUEUE: ",avgQ)
        print("AVERAGE NUMBER IN SYSTEM: ",avgS)



    # def pgf(self):
    #     self.n_arrival += 1
    #     self.status = 'busy'
    #     if self.cqs < self.maxque:
    #         self.id+=1
    #         hq.heappush(self.inq,(self.id,self.at))         # store packet id and arrival time
    #         self.at = self.simclock + self.pg()             # prepare new packet arrival time

    #         if len(self.sink) < 1:
    #             hq.heappush(self.sink,hq.heappop(self.inq))
    #             if self.cqs <= 1:
    #                 self.st1 = self.sg()                    #service time
    #                 print(">>>>Service time>>>>",self.st1)
    #                 self.dt = self.simclock + self.st1
    #         else:
    #             self.cqs += 1
    #     else:
    #         self.npdrop += 1
    #         self.at = self.simclock + self.pg()


    # def pdf(self):
    #     self.status = 'idle'
    #     hq.heappop(self.sink)                                   # packet departed from server
    #     self.n_depart+=1                                        # no of packet depart increase
    #     self.npdelay+=1
    #     self.cqs -=1
    #     if self.cqs >= 0:
    #         self.t2 = hq.heappop(self.inq)
    #         self.tmpd = self.t2[1]                              # get value to calculate delay
    #         self.calc_delay(self.dt,self.tmpd)                  # calculate total delay  
    #         hq.heappush(self.sink,self.t2)                      # move packet from queue to server
    #         self.st2 = self.sg()                                # set new service time
    #         print(">>>>Service time<<<<",self.st2)
    #         self.dt = self.simclock + self.st2                  # set time for packet departure
    #     else:
    #         self.cqs +=1
    #         self.dt = float('inf')

    # def calc_delay(self,depT,arrT):
    #     self.tdelay = self.tdelay + (depT - arrT)


    # def result(self):
    #     self.plr = self.npdrop/self.n_arrival
    #     self.avgdelay = self.tdelay/self.npdelay
    #     print("Packet loss rate: ",self.plr)
    #     print("Total delay time: ",self.tdelay)
    #     print("No of packet delay: ",self.npdelay)
    #     print("Average delay: ", self.avgdelay) 


    def pg(self):
        #return 0.1
        return np.random.exponential(1/8)
        
        # print(self._iat)
        # return self._iat.pop(0)

    def sg(self):
        return np.random.exponential(1/9)
        # x = self._dpt.pop(0)
        # return x

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

class fifo:
    def __init__(self,maxQ,evt):
        self._que = []
        self.maxQ = maxQ
        self.evt = evt
        # self.serber = Server()


    # def runFifo(self):
    #     if self.evt.getType()== 'arrive':
    #         if len(self._que)< self.maxQ:
    #             self.enQ(self.evt.getTime())
    #             self.at 
    #             if self.serber.checkServer() == 'idle':
    #                 self.serber.inServer(self.deQ())
            


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

        
if __name__ == "__main__":
    
    a = simulation()
    x = 99999 
    np.random.seed(0)
    for i in range(x):
        a.scheduling()
        a.uclock()
        #a.que()
        # a.server()
        a.etype()
    a.reportGeneration()
    # a.result()
    
    
