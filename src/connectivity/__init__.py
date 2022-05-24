#!/usr/bin/python3

from . import db
import hashlib

from src.constants import AUCTION_REQUESTS_LIST_APPROVED
from src.constants import AUCTION_REQUESTS_LIST_BOTH
from src.constants import MESSAGE_KEY_FROM
from src.constants import MESSAGE_KEY_TO
from src.constants import USER_ROLE_ADMIN
from src.constants import USER_ROLE_MANAGER
from src.constants import USER_ROLE_USER

def enc(m):
	"""
	takes a parameter and make a hash of it
	using SHA256 algorithm
	"""
	return hashlib.sha256(m.encode('utf-8')).hexdigest()

def check_password(username, password):
	"""
	takes username and newpass
	and returns True or False after password verification
	"""
	return db.verify_password(username, enc(password))


def create_account(fname, lname, username, pan,  password, secques, secans):
	"""
	takes fname, lname, username, pan,  password, secques, secans
	to create a new account
	"""
	return db.create_user(fname, lname, username, pan,  enc(password), secques, enc(secans))

def get_user_id(username):
	"""
	takes username
	and returns user_id for it
	"""
	return str(db.get_user_details_by_username(username)['id'])

def get_user_details(username):
	return db.get_user_details_by_username(username)

def get_username(user_id):
	return db.get_user_details_by_id(user_id)['username']

def get_user_by_id(user_id):
	return db.get_user_details_by_id(user_id)

def validate_username(username):
	"""
	takes username
	and returns True if username exists
	"""
	return db.check_user_exists(username)

def fetch_security_question(username):
	"""
	takes username
	and returns sequrity question for it
	"""
	return db.get_security_question(username)

def validate_security_answer(username, answer):
	"""
	takes username and answer
	and returns True if security answer
	is correct for the given username
	"""
	return db.verify_security_answer(username, enc(answer))

def update_password(username, pass1):
	"""
	takes username and newpass
	to update password of a username
	"""
	return db.update_password(username, enc(pass1))


def approve_auction_id(req_id, approved_by_id):
	"""
	takes requst_id and approved_by_id
	and returns auction_id if approved sucessfully
	else returns None
	
	"""
	b, ret = db.approve_an_auction_request(req_id, approved_by_id)
	if b is False:
		return None
	return ret


def reject_auction_id(req_id, rejected_by):
	"""
	takes requst_id and rejected_by_id
	and returns auction_id if approved sucessfully
	else returns None
	
	"""
	return db.reject_an_auction_request(req_id, rejected_by)

def create_auction_requst(seller_id, title, description, quantity, min_price):
	"""
	takes seller_id, title, description, quantity, min_price
	and returns requst_id of auction request
	"""
	return db.create_auction_request_id(seller_id, title, description, quantity, min_price)


def get_auctions_list():
	return db.get_auction_list()

def get_auction_details(auction_id):
	return db.get_auction_details(auction_id)

def get_auction_requests_unapproved():
	return db.get_auction_request()

def get_auction_requests_approved():
	return db.get_auction_request(AUCTION_REQUESTS_LIST_APPROVED)

def get_auction_requests_both():
	return db.get_auction_request(AUCTION_REQUESTS_LIST_BOTH)


def send_message(fr, t, sub, data):
	return db.add_new_message(fr, t, sub, data)

def list_messages_from(user_id):
	return db.get_messages(key=MESSAGE_KEY_FROM, value=user_id)

def list_messages_to(user_id):
	return db.get_messages(key=MESSAGE_KEY_TO, value=user_id)


def make_manager(manager_id):
	return db.set_user_role(user_id=manager_id, role=USER_ROLE_MANAGER)

def make_administrator(admin_id):
	return db.set_user_role(user_id=admin_id, role=USER_ROLE_ADMIN)

def make_normal_user(user_id):
	return db.set_user_role(user_id=user_id, role=USER_ROLE_USER)

def get_role(user_id):
	return db.get_user_role(user_id)

def get_requests_list_by_id(uid, mode):
	return db.get_requests_list_by_id(uid, mode)

def get_requests_list_by_id_both(uid):
	return db.get_requests_list_by_id(uid, AUCTION_REQUESTS_LIST_BOTH)

def getuser(uname):
	return db.getuser(uname)




def save_auction_times(auction_id, start, end):
	return db.save_auction_details(auction_id, start, end)

def status_auction(auction_id):
	return db.status_auction(auction_id)

def cancel_auction(uid, auction_id):
	return db.cancel_auction(uid, auction_id)



def cancel_bid(participant_id, auction_id):
	return db.cancel_bid(participant_id, auction_id)

def make_bid(bidder_id, auction_id, qty, ppi, amt, finalPayment):
	return db.make_bid(bidder_id, auction_id, qty, ppi, amt, finalPayment)


def getBidInfo(bid_id):
	return db.get_BidInfo(bid_id)



def create_payout(tid, seller_oreder_id):
	return db.create_payout(tid, seller_oreder_id)

def update_payouts(tid, seller_trans_id, payment_status):
	return db.update_payouts(tid, seller_trans_id, payment_status)

def get_payout_list():
	return db.get_payout_list()



def update_payments(order_id, trans_id, payment_status):
	return db.update_payments(order_id, trans_id, payment_status)

def create_payment(order_id, bid_id, auction_id, qty, ppi, amt, fPay):
	return db.create_payment(order_id, bid_id, auction_id, qty, ppi, amt, fPay)


def loopbody1():
	list_max = Init()
	for bid in get_bid_list():
		if bid['auction_id'] in list_max.get_keys():
			t = list_max.get(bid['auction_id'])
			m = getMax(bid, t)
			list_max.set(bid['auction_id'], m)
		else:
			list_max.insert(bid['auction_id'], bid)
	for i in list_max.get_list():
		if i['msg_sent'] == '':
			sendBotMsg(i)
			create_trans_for_bid_id(i)


def loopbody2():
	time_now = datetime.datetime.utc_now()
	for i in get_trans_list():
		t = i['init_time']
		t1 = datetime.datetime(t)
		if i['bidder_paid'] == 'NOT PAID':
			if not validate_time(t, time_now):
				remove_trans_details(i['id'])
				sendLateMsg(i['bid_id'])
				removeBid(i['bid_id'])


def loopbody3():
	bid_list = get_bid_list()
	auction_list = get_auctions_list()
	
	for i in auction_list:
		exist = False
		for j in bid_list:
			if i['id'] == j['auction_id']:
				exist = True
		if not  exist:
			setAuctionFailed(i['id'])
			sendMsgAuctionFailed(i['seller_id'], i['id'])


def get_bid_list():
	pass

def sendMsgAuctionFailed(seller_id, auction_id):
	pass

def setAuctionFailed(auction_id):
	pass


class Init():
	pass

def getMax(b1, b2):
	pass

def sendBotMsg(b):
	pass

def create_trans_for_bid_id(b):
	pass



def get_trans_list():
	pass

def validate_time(time, time_now):
	pass

def remove_trans_details(trans_id):
	pass

def sendLateMsg(bid_id):
	pass

def removeBid(bid_id):
	pass


def generate_order_id(auction_id, bid_id):
	return 'TO BE IMPLEMENTED'


