#!/usr/bin/python3

class UserClass(object):

	def __init__(self, fname, lname, username, uid, role):
		self.fname = fname
		self.lname = lname
		self.username = username
		self.role = role
		self.uid = uid
	
	def get_name(self):
		return self.fname + ' ' + self.lname
	
	def get_username(self):
		return self.username
	
	def get_role(self):
		return self.role
	
	def get_uid(self):
		return self.uid


