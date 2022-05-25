#!/usr/bin/python3

class BidInfo:
	def __init__(self, bid_id, qty, ppi, amt, fpay):
		self._bid_id = bid_id
		self._qty = qty
		self._ppi = ppi
		self._amt = amt
		self._fpay = fpay
	
	def getBidId(self):
		return self._bid_id
	
	def getQuantity(self):
		return self._qty
	
	def getPricePerItem(self):
		return self._ppi
	
	def getAmount(self):
		return self._amt
	
	def getFPay(self):
		return self._fpay


