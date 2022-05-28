#!/usr/bin/python3

import sqlite3
import hashlib

from multiprocessing import Lock

import click
from flask import current_app, g
from flask.cli import with_appcontext
from src.connectivity.userclass import UserClass
from src.connectivity.BidInfo import BidInfo

from src.constants import AUCTION_REQUESTS_LIST_NOT_APPREVED
from src.constants import AUCTION_REQUESTS_LIST_BOTH
from src.constants import MESSAGE_KEY_TO
from src.constants import USER_ROLE_ADMIN
from src.constants import USER_ROLE_MANAGER
from src.constants import ADMIN_USERNAME
from src.constants import ADMIN_PASSWORD
from src.constants import BOT_USERNAME
from src.constants import BOT_PASSWORD


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
		current_app.config['DATABASE'],#DATABASE,
		detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db

def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.commit()
		db.close()

def init_db():
	db = get_db()
	with current_app.open_resource(current_app.config['DATABASE_SCHEMA']) as f:
		db.executescript(f.read().decode('utf-8'))

def create_admin_user():
	admin_pass = hashlib.sha256(ADMIN_PASSWORD.encode('utf-8')).hexdigest()
	admin_answer = hashlib.sha256('admin'.encode('utf-8')).hexdigest()
	if create_user('Admin', 'Admin', ADMIN_USERNAME, 'admin',  admin_pass, 'admin', admin_answer):
		admin_id = get_user_details_by_username(ADMIN_USERNAME)['id']
		set_user_role(admin_id, USER_ROLE_ADMIN)

def create_bot_user():
	bot_pass = hashlib.sha256(BOT_PASSWORD.encode('utf-8')).hexdigest()
	bot_answer = hashlib.sha256('BOT'.encode('utf-8')).hexdigest()
	if create_user('Bot', 'Bot', BOT_USERNAME, 'Bot',  bot_pass, 'Bot', bot_answer):
		bot_id = get_user_details_by_username(BOT_USERNAME)['id']
		set_user_role(bot_id, USER_ROLE_MANAGER)



@click.command('init_db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initializing the Database...')
	create_admin_user()
	click.echo('Creating Admin user...')
	create_bot_user()
	click.echo('Creating Bot user...')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

def execute(sql):
	l = Lock()
	l.acquire()
	dba = get_db()
	try:
		r = dba.execute(sql).lastrowid
		dba.commit()
		l.release()
		return r
	except sqlite3.IntegrityError:
		l.release()
		return -1
	except sqlite3.OperationalError:
		print(sql)
		l.release()
		return -1
	except TypeError:
		l.release()
		return -1

def create_user(fname, lname, username, pan,  password, secques, secans):
	sql = f"INSERT INTO user (fname, lname, username, pan_no,  password, secques, secans) VALUES ('{fname}', '{lname}', '{username}', '{pan}',  '{password}', '{secques}', '{secans}');"
	return False if execute(sql) == -2 else True

def verify_password(username, password):
	dbase = get_db()
	sql = f"SELECT password FROM user WHERE username='{username}';"
	res = dbase.execute(sql).fetchone()
	if res is None:
		return False
	return res[0] == password

def get_bot_id():
	sql = "SELECT id FROM user;"
	dbase = get_db()
	return dbase.execute(sql).fetchone()['id']


def get_users_list():
	sql = "SELECT id, fname, lname, username, pan_no, secques, role, address FROM user;"
	dbase = get_db()
	return dbase.execute(sql).fetchall()

def get_user_details_by_username(username):
	dbase = get_db()
	sql = f"SELECT * FROM user WHERE username='{username}';"
	return dbase.execute(sql).fetchone()

def get_user_details_by_id(user_id):
	dbase = get_db()
	sql = f"SELECT * FROM user WHERE id ='{user_id}';"
	return dbase.execute(sql).fetchone()

def get_user_role(user_id):
	dbase = get_db()
	sql = f"SELECT role FROM user WHERE id='{user_id}';"
	r = dbase.execute(sql).fetchone()
	#dbase.close()
	if r is None:
		return -1
	return r[0]

def set_user_role(user_id, role):
	sql = f"UPDATE user SET role = '{role}' WHERE id = '{user_id}';"
	execute(sql)

def check_user_exists(username):
	dbase = get_db()
	sql = f"SELECT username FROM user WHERE username='{username}';"
	r = dbase.execute(sql).fetchone()
	#dbase.close()
	if r is not None:
		return True
	return False

def get_security_question(username):
	dbase = get_db()
	sql = f"SELECT secques FROM user WHERE username='{username}';"
	r = dbase.execute(sql).fetchone()
	#dbase.close()
	if r is not None:
		return r[0]
	return None

def verify_security_answer(username, answer):
	dbase = get_db()
	sql = f"SELECT secans FROM user WHERE username='{username}';"
	r = dbase.execute(sql).fetchone()
	#dbase.close()
	if r is not None:
		return r[0] == answer
	return False

def update_address(user_id, address):
	sql = f"UPDATE user SET address = '{address}' WHERE id = '{user_id}';"
	execute(sql)

def update_mobile(user_id, mobile):
	sql = f"UPDATE user SET mobile = '{mobile}' WHERE id = '{user_id}';"
	execute(sql)

def update_email(user_id, email):
	sql = f"UPDATE user SET email = '{email}' WHERE id = '{user_id}';"
	execute(sql)

def update_name(user_id, fname, lname):
	sql = f"UPDATE user SET fname = '{fname}', lname = '{lname}' WHERE id = '{user_id}' ;"
	execute(sql)

def update_secqa(user_id, secq, seca):
	sql = f"UPDATE user SET secques = '{secq}', secans = '{seca}' WHERE id = '{user_id}';"
	execute(sql)

def update_password(username, password):
	sql = f"UPDATE user SET password = '{password}' WHERE username = '{username}';"
	execute(sql)
	return verify_password(username, password)

def create_auction_request_id(seller_id, title, description, quantity, min_price):
	sql = f"INSERT INTO auction_requests (seller_id, title, description, quantity, min_price) VALUES ({seller_id}, '{title}', '{description}', {quantity}, {min_price});"
	return execute(sql)

def approve_an_auction_request(request_id, approved_by):
	sql1 = f"UPDATE auction_requests SET approved = 1, response_by = {approved_by} WHERE id = {request_id};"
	sql2 = f"SELECT seller_id, id, created, title, description, quantity, min_price FROM auction_requests WHERE id = {request_id};"
	execute(sql1)
	dbase = get_db()
	seller_id, req_id, created, title, description, quantity, min_price = dbase.execute(sql2).fetchone()
	sql3 = f"INSERT INTO auction_list (seller_id, request_id, created, approved_by, title, description, quantity, min_price) VALUES ('{seller_id}', '{req_id}', '{created}', '{approved_by}', '{title}', '{description}', '{quantity}', '{min_price}');"
	return execute(sql3)

def reject_an_auction_request(request_id, rejected_by_id):
	sql1 = f"UPDATE auction_requests SET approved = -1, response_by = {rejected_by_id} WHERE id = {request_id};"
	sql2 = f"DELETE FROM auction_list WHERE request_id = {request_id};"
	r1 = execute(sql1)
	r2 = execute(sql2)
	return True if r1 != -1 or r2 != -1 else False

def get_auction_list():
	sql = "SELECT * FROM auction_list;"
	return get_db().execute(sql).fetchall()

def get_auction_details(auction_id):
	sql = f"SELECT * FROM auction_list WHERE id = '{auction_id}';"
	return get_db().execute(sql).fetchone()


def get_auction_request(mode=AUCTION_REQUESTS_LIST_NOT_APPREVED):
	sql = "SELECT * FROM auction_requests WHERE approved=0 OR approved=1 OR approved=-1  ORDER BY approved ASC,id DESC;" if mode == AUCTION_REQUESTS_LIST_BOTH else f"SELECT * FROM auction_requests WHERE approved={mode} ORDER BY approved ASC,id DESC;"
	return get_db().execute(sql).fetchall();

def get_requests_list_by_id(uid, mode=AUCTION_REQUESTS_LIST_NOT_APPREVED):
	sql = f"SELECT * FROM auction_requests WHERE seller_id = '{uid}'  ORDER BY approved ASC,id DESC;" if mode == AUCTION_REQUESTS_LIST_BOTH else f"SELECT * FROM auction_requests WHERE seller_id = '{uid}',approved={mode} ORDER BY approved ASC,id DESC;"
	return get_db().execute(sql).fetchall();

def add_new_message(f, t, sub, msg):
	sql = f"INSERT INTO msg(msg_from, msg_to, msg_subject, msg_data) VALUES ({f}, {t}, '{sub}', '{msg}');"
	execute(sql)

def get_messages(key=MESSAGE_KEY_TO, value=-1):
	sql = f"SELECT msg_subject, created, msg_from, msg_to, msg_data FROM msg WHERE {key} = {value} ORDER BY created DESC;"
	return get_db().execute(sql).fetchall()


def getuser(username):
	dbase = get_db()
	sql = f"SELECT fname, lname, username, id, role FROM user WHERE username ='{username}';"
	r = dbase.execute(sql).fetchone()
	if r == None:
		return None
#	return UserClass(r[0], r[1], r[2], r[3], r[4])
	return UserClass(r['fname'], r['lname'], r['username'], r['id'], r['role'])

def save_auction_details(auction_id, start_time, end_time):
	sql = f"UPDATE auction_list SET start_datetime = '{start_time}', end_datetime = '{end_time}', finalized = 1 WHERE id = {auction_id};"
	execute(sql)

def status_auction(auction_id):
	dbase = get_db()
	sql = f"SELECT status FROM auction_list WHERE id = {auction_id};"
	return dbase.execute(sql).fetchone()

def cancel_auction(uid, auction_id):
	sql = f"UPDATE auction_list SET status = -2 WHERE id = {auction_id} AND seller_id = {uid};"
	execute(sql)
	return 1

def cancel_bid(participant_id, auction_id):
	sql = f"DELETE FROM bids WHERE participant_id = '{participant_id}' AND auction_id = '{auction_id}' ;"
	execute(sql)

def make_bid(bidder_id, auction_id, qty, ppi, amt, finalPayment):
	sql1 = f"SELECT id FROM bids WHERE participant_id = '{bidder_id}' AND auction_id = '{auction_id}' ;"
	dbase = get_db()
	r = dbase.execute(sql1).fetchone()
	if r is not None:
		sql2 = f"UPDATE bids SET qty = '{qty}', ppi= '{ppi}', amt = '{amt}', fPay = '{finalPayment}' WHERE id = '{r[0]}' ;"
		execute(sql2)
		return r[0]
	sql3 = f"INSERT INTO bids (participant_id, auction_id, qty, ppi, amt, fPay) VALUES ('{bidder_id}', '{auction_id}', '{qty}', '{ppi}', '{amt}', '{finalPayment}');"
	return execute(sql3)

def get_BidInfo(bid_id):
	dbase = get_db()
	sql = f"SELECT qty, ppi, amt, fpay FROM bids WHERE id = '{bid_id}' ;"
	r = dbase.execute(sql).fetchone()
	return BidInfo(bid_id, r[0], r[1], r[2], r[3])

def create_payment(order_id, bid_id, auction_id, qty, ppi, amt, fPay):
	sql = f"INSERT INTO  trans (order_id, bid_id, auction_id, qty, ppi, amt, seller_Pay) VALUES ('{order_id}', '{bid_id}', '{auction_id}', '{qty}', '{ppi}', '{amt}', '{fPay}') ;"
	return execute(sql)

def update_payments(order_id, trans_id, payment_status):
	if payment_status == 'SUCESS':
		sql = f"UPDATE trans SET trans_id = '{trans_id}', bidder_paid = 'PAID' WHERE order_id = '{order_id}' ;"
		execute(sql)

def get_payout_list():
	dbase = get_db()
	sql = f"SELECT * FROM trans WHERE seller_paid = 'NOT PAID' AND bidder_paid = 'PAID' ;"
	return dbase.execute(sql).fetchall()

def create_payout(tid, seller_oreder_id):
	sql = f"UPDATE trans SET seller_order_id = '{seller_order_id}' WHERE id = '{tid}' ;"
	execute(sql)

def update_payouts(tid, seller_trans_id, payment_status):
	if payment_status == 'SUCESS':
		sql = f"UPDATE trans seller_trans_id = '{seller_trans_id}', seller_paid = 'PAID' WHERE id = '{tid}' ;"
		execute(sql)


def removeBid(bid_id):
	sql = f"DELETE FROM bids WHERE id = {bid_id};"
	execute(sql)

def get_bid_list():
	sql = "SELECT * FROM bids;"
	dbase = get_db()
	return dbase.execute(sql).fetchall()

def setAuctionFailed(auction_id):
	sql1 = f"DELETE FROM trans WHERE auction_id = {auction_id} ;"
	sql2 = f"DELETE FROM bids WHERE auction_id = {auction_id} ;"
	sql3 = f"UPDATE auction_list SET status = -1 WHERE id = {auction_id} ;"
	execute(sql1)
	execute(sql2)
	execute(sql3)

def remove_trans_details(trans_id):
	sql = f"DELETE FROM trans WHERE id = {trans_id}"
	execute(sql)

def get_trans_list():
	sql = "SELECT * FROM trans;"
	return get_db().execute(sql).fetchall()

def get_order_id(auction_id, bid_id):
	sql = f"SELECT order_id FROM trans WHERE auction_id = '{auction_id}' AND bid_id = '{bid_id}' ;"
	return get_db().execute(sql).fetchone()['order_id']

def get_trans_history():
	sql = "SELECT * FROM trans WHERE bidder_paid = 'PAID';"
	return get_db().execute(sql).fetchall()

def setMsgSent(bid_id):
	sql = f"UPDATE bids SET msg_sent = 'SENT' WHERE id = '{bid_id}' ;"
	execute(sql)


def get_seller_by_auction_id(auction_id):
	sql = f"SELECT seller_id FROM auction_list WHERE id = '{auction_id}' ;"
	return get_db().execute(sql).fetchone()

def get_auctions_by_seller_id(seller_id):
	sql = f"SELECT id FROM auction_list WHERE seller_id = '{seller_id}' ;"
	return get_db().execute(sql).fetchall()


