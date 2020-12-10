import numpy as np
import pandas as pd
import seaborn as sns

class simulation:
	def __init__(self):
		self.sstatus = 0 #initial server status 0 is not busy
		self.simclock = 0.00 #simclock
		self.arrt = self.packet_generation() #call packet arrival function
		self.dept = self.packet_departure() #call packet departure function
		self.nodes = int(input('insert nodes:'))
		self.npa = 0 #no of packet arrival
		self.npd = 0 #no of packet departed
		self.servt = self.service_time() #call service time function
		self.delay = 0 #delay
		self.npdl = 0 #no of packet delay
		self.cqs = 0 #current que size
		self.tqs = 0 #total que size
		self.mqs = int(input('insert que size:')) #max que size

	def packet_generation(self):
		return np.random.lognormal(mean=0.6, sigma=0.3)

	def service_time(self):
		return np.random.uniform(low = 5, high = 8)



"""
def initialize():
	nodes = input('insert ')
	tarrival = []
	tservice  = []
	cdelay = 0
	simclock = 0
	snodes = int(nodes)
	nque = 0
	nque_max = 4
	sstatus = False
	eventype = 'arrival'

	for i in range(0,snodes):
		atemp = round(r.uniform(0.00,2),2)
		dtemp = round(r.uniform(0.00,2),2)
		tarrival.append(atemp)
		tservice.append(dtemp)"""

#def scheduler(x,y,z):

