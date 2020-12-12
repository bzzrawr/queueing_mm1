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

class sim:
    def __init__(self):
        self._simclock = None
        self.t_arrival = 0
        self.t_depart = 0
        self.t_service = 0
        self._maxque = None
        self.cqs = 0
        self.sstatus = 0
        self.nodes = None

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
                try:
                    self._maxque = int(self._maxque)
                except:
                    self._maxque = None
                    print("Insert valid integer!")

        t_event = min(self.t_arrival,self.t_depart)
        self.simclock = t_event
        print("current time:",self.simclock)
        print("arrival time:",self.t_arrival,"departure time:",self.t_depart)
        
        if self.t_arrival <= self.t_depart:
            self.arrival_event()
        else:
            self.depart_event()

