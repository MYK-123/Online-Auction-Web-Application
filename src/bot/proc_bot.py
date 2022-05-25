#!/usr/bin/python3

from src.connectivity import loopbody1
from src.connectivity import loopbody2
from src.connectivity import loopbody3

from multiprocessing import Process, Value

class Bot(Process):
	is_running = False
	def run(self):
		while is_running:
			loopbody1()
			loopbody2()
			loopbody3()

	def start(self):
		is_running = True
		super.start()

	def set_deamon(self, d):
		self.deamon = d


