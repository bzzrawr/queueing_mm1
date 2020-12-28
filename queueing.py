import heapq as hq
import numpy as np

class simulation(object):
    def __init__(self):
        self.simclock = 0.0     #simulation clock
        self.at = 0.4           #packet arrival time
        self.dt = float('inf')  #packet departure time
        self.et = 0.0           #event time
        self.sink = []          #current packet in the server
        self.n_arrival = 0      #no of packet arrival
        self.n_depart = 0       #no of packet departure
        self.npdrop = 0         #no of packet drop
        self.id = 0             #packet id
        self.status = 'idle'    #server status
        self.cqs = 0            #current queue size
        self.maxque = int(input("Enter maximum que:")) #maximum queue size
        self._iat = [1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9,0.8]
        self._dpt = [2.0,0.7,0.2,1.1,3.7,0.6,float('inf')]
        self.tdelay = 0.0       #total delay
        self.inq = []           #packet in the queue
        self.tmpd = 0.0         #temp value for calculating delay
        self.t2 = None          #temp value for calculating delay
        self.avgdelay = 0       #average delay
        self.plr = 0.0          #packet loss rate
        self.npdelay = 1        #no of packet delayed


    def scheduling(self):
        self.et = min(self.at,self.dt)  #scheduling for event timeq
        print("server status: ",self.status)
        print("Currently in queue: ",self.cqs)
        print("Packet in server: ",self.sink)
        print("Packet in queue: ",self.inq)
        print("No of packet arrived: ",self.n_arrival)
        print("No of packet departed: ",self.n_depart)
        print("No of packet dropped: ",self.npdrop)
        print("event time:",self.et)
        print("arrival time:",self.at,"departure time:",self.dt)
        print("------------------------------------------------")


    def uclock(self):
        self.simclock = self.et

        

    def etype(self):
        if self.at <= self.dt:
            self.pgf()
        else:
            self.pdf()


    def pgf(self):
        self.n_arrival += 1
        self.status = 'busy'
        if self.cqs < self.maxque:
            self.id+=1
            hq.heappush(self.inq,(self.id,self.at))         # store packet id and arrival time
            self.at = self.simclock + self.pg()             # prepare new packet arrival time

            if len(self.sink) < 1:
                hq.heappush(self.sink,hq.heappop(self.inq))
                if self.cqs <= 1:
                    self.st1 = self.sg()                    #service time
                    print(">>>>Service time>>>>",self.st1)
                    self.dt = self.simclock + self.st1
            else:
                self.cqs += 1
        else:
            self.npdrop += 1
            self.at = self.simclock + self.pg()


    def pdf(self):
        self.status = 'idle'
        hq.heappop(self.sink)                                   # packet departed from server
        self.n_depart+=1                                        # no of packet depart increase
        self.npdelay+=1
        self.cqs -=1
        if self.cqs >= 0:
            self.t2 = hq.heappop(self.inq)
            self.tmpd = self.t2[1]                              # get value to calculate delay
            self.tdelay = self.tdelay + (self.dt - self.tmpd)   # calculate total delay
            hq.heappush(self.sink,self.t2)                      # move packet from queue to server
            self.st2 = self.sg()                                # set new service time
            print(">>>>Service time<<<<",self.st2)
            self.dt = self.simclock + self.st2                  # set time for packet departure
        else:
            self.cqs +=1
            self.dt = float('inf')


    def result(self):
        self.plr = self.npdrop/self.n_arrival
        self.avgdelay = self.tdelay/self.npdelay
        print("Packet loss rate: ",self.plr)
        print("Total delay time: ",self.tdelay)
        print("No of packet delay: ",self.npdelay)
        print("Average delay: ", self.avgdelay)


    def pg(self):
        #return 0.1
        #return round((np.random.exponential(1/6)),2)
        
        print(self._iat)
        return self._iat.pop(0)

    def sg(self):
        #return round((np.random.exponential(1/3)),2)
        x = self._dpt.pop(0)
        return x


if __name__ == "__main__":
    
    a = simulation()
    x = 14
    for i in range(x):
        a.scheduling()
        a.uclock()
        #a.que()
        # a.server()
        a.etype()
    a.result()
    
    
