import random as r

class sim:
    def __init__(self):
        self._simclock = None
        self.t_arrival = self.g_packet()    
        self.t_depart = float('inf')
        self.t_service = 0
        self._maxque = None
        self.cqs = 0
        self.sstatus = 0
        self.nodes = None
        self.npdrop = 0
        self.n_depart = 0
        self.t_event = 0
        self.n_arrival = 0
        self.tmp_time = self.g_service()

    #def sch(self):
     #   print(1)
            
    def a_event(self):
        self.sstatus += 1
        self.n_arrival += 1
        if self.sstatus <= 1:
            self.temp1 = self.g_service()
            print(">>>>Service time>>>>",self.temp1)
            self.tmp_time=self.temp1
            self.t_depart = self.simclock + self.temp1
        self.t_arrival = self.simclock + self.g_packet()

    def d_event(self):
        self.sstatus -=1
        self.n_depart += 1
        if self.sstatus > 0:
            self.temp2=self.g_service()
            print(">>>>Service time<<<<",self.temp2)
            self.tmp_time = self.temp2
            self.t_depart = self.simclock + self.temp2
        else:
            self.t_depart = float('inf')

    def u_clock(self):
        self.t_event = min(self.t_arrival,self.t_depart)
        self.simclock = self.t_event
    
        print("event time:",self.simclock)
        print("arrival time:",self.t_arrival,"departure time:",self.t_depart)
        print('---------------------------')
            
    def event_type(self):
        if self.t_arrival <= self.t_depart:
            self.a_event()
        else:
            self.d_event()

    def g_service(self):
        return round(r.uniform(0,2),2)

    def g_packet(self):
        return round(r.uniform(0,2),2)

    def s_nq(self):
        
        if self.nodes is None:
            while self.nodes is None:
                self.nodes = input("Insert number of nodes:")
                try:
                    self.nodes = int(self.nodes)
                except:
                    self.nodes = None
                    print("Insert valid integer!")
        if self._maxque is None:
            while self._maxque is None:
                self._maxque = input("Insert maximum que size:")
                print('---------------------------')
                try:
                    self._maxque = int(self._maxque)
                except:
                    self._maxque = None
                    print("Insert valid integer!")
                    
        return self.nodes

    @property
    def simclock(self):
        return self._simclock

    @simclock.setter
    def simclock(self,clock):
        self._simclock = clock

    def ssc(self):
        print("sstatus number",self.sstatus)
        

if __name__ == "__main__":
    
    a = sim()
    x = a.s_nq()
    for i in range(0,x):
        #a.sch()
        a.ssc()
        a.u_clock()
        a.event_type()
