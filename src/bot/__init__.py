#!/usr/bin/python3

import time

from src.connectivity import loopbody1
from src.connectivity import loopbody2
from src.connectivity import loopbody3

from multiprocessing import Process, Value

class Bot(Process):
	is_running = False
	def run(self):
		while self.is_running:
			with self.cxt:
				loopbody1()
				loopbody2()
				loopbody3()
				time.sleep(3)
	
	def context(self, app_cxt):
		self.cxt = app_cxt
	
	def start(self):
		self.is_running = True
		super().start()

	def set_deamon(self, d):
		self.deamon = d


def start_bot(app_cxt, daemon=True):
	bot = Bot()
	bot.context(app_cxt)
	bot.daemon = daemon
	time.sleep(5)
	bot.start()


