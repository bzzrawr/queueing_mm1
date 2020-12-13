import numpy as np
import pandas as pd
import seaborn as sns

# class simulation:
# 	def __init__(self):
# 		self.sstatus = 0 #initial server status 0 is not busy
# 		self.simclock = 0.00 #simclock
# 		self.arrt = self.packet_generation() #call packet arrival function
# 		self.dept = self.packet_departure() #call packet departure function
# 		self.nodes = int(input('insert nodes:'))
# 		self.npa = 0 #no of packet arrival
# 		self.npd = 0 #no of packet departed
# 		self.servt = self.service_time() #call service time function
# 		self.delay = 0 #delay
# 		self.npdl = 0 #no of packet delay
# 		self.cqs = 0 #current que size
# 		self.tqs = 0 #total que size
# 		self.mqs = int(input('insert que size:')) #max que size

# 	def packet_generation(self):
# 		return np.random.lognormal(mean=0.6, sigma=0.3)

# 	def service_time(self):
# 		return np.random.uniform(low = 5, high = 8)

class sim(que):
    def __init__(self):
        que.__init__(self)
        self.st = self.g_packet()
        self._simclock = None
        self.t_arrival = 0
        self.t_depart = 0
        self.t_service = 0        
        self.cqs = 0
        self.sstatus = None
        self.nodes = None
        self.npdrop = 0
        self.n_depart = 0
        self.t_event = 0
        self.tmp_time = self.g_service()

    def sch(self):

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
                    
        self.t_event = min(self.t_arrival,self.t_depart)


    def update_clock(self):
        self.simclock = self.t_event


    def g_service(self):
        return round(r.uniform(0,2),2)

    def g_packet(self):
        return round(r.uniform(0,2),2)
            
    def event_type(self):
        if self.t_arrival <= self.t_depart:
            self.arrival_event()

        else:
            self.depart_event()

