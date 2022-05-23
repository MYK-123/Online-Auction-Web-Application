#!/usr/bin/python3

import sqlite3
import hashlib

import click
from flask import current_app, g
from flask.cli import with_appcontext
from src.connectivity.userclass import UserClass

from src.constants import AUCTION_REQUESTS_LIST_NOT_APPREVED
from src.constants import AUCTION_REQUESTS_LIST_BOTH
from src.constants import MESSAGE_KEY_TO
from src.constants import USER_ROLE_ADMIN
from src.constants import ADMIN_USERNAME
from src.constants import ADMIN_PASSWORD


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


@click.command('init_db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initializing the Database...')
	create_admin_user()
	click.echo('Creating Admin user...')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

def execute(dba, sql):
	if dba is not None:
		print(sql)
		r = dba.execute(sql).fetchall()
		dba.commit()
#		close_db(dba)
		return r
	return None

def create_user(fname, lname, username, pan,  password, secques, secans):
	dbase = get_db()
	sql = f"INSERT INTO user (fname, lname, username, pan_no,  password, secques, secans) VALUES ('{fname}', '{lname}', '{username}', '{pan}',  '{password}', '{secques}', '{secans}');"
	try:
		r = dbase.execute(sql)
		dbase.commit()
		return True
	except sqlite3.IntegrityError:
		return False


def verify_password(username, password):
	dbase = get_db()
	sql = f"SELECT password FROM user WHERE username='{username}';"
	res = dbase.execute(sql).fetchone()
	if res is None:
		return False
	return res[0] == password

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
	dbase = get_db()
	sql = f"UPDATE user SET role = '{role}' WHERE id = '{user_id}';"
	dbase.execute(sql).fetchone()
	dbase.commit()


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

def update_password(username, password):
	dbase = get_db()
	sql = f"UPDATE user SET password = '{password}' WHERE username = '{username}';"
	r = dbase.execute(sql).fetchone()
	dbase.commit()
	#dbase.close()
	return verify_password(username, password)

def create_auction_request_id(seller_id, title, description, quantity, min_price):
	dbase = get_db()
	sql = f"INSERT INTO auction_requests (seller_id, title, description, quantity, min_price) VALUES ({seller_id}, '{title}', '{description}', {quantity}, {min_price});"
	cur = dbase.cursor()
	r = cur.execute(sql)
	dbase.commit()
	#dbase.close()
	return r.lastrowid

def approve_an_auction_request(request_id, approved_by):
	dbase = get_db()
	try:
		sql1 = f"UPDATE auction_requests SET approved = 1, response_by = {approved_by} WHERE id = {request_id};"
		sql2 = f"SELECT seller_id, id, created, title, description, quantity, min_price FROM auction_requests WHERE id = {request_id};"
		dbase.execute(sql1)
		seller_id, req_id, created, title, description, quantity, min_price = dbase.execute(sql2).fetchone()
		sql3 = f"INSERT INTO auction_list (seller_id, request_id, created, approved_by, title, description, quantity, min_price) VALUES ('{seller_id}', '{req_id}', '{created}', '{approved_by}', '{title}', '{description}', '{quantity}', '{min_price}');"
		r = dbase.execute(sql3).lastrowid
	except sqlite3.IntegrityError:
#		dbase.close()
		return False, -1
	except  TypeError:
#		dbase.close()
		return False, -1
	else:
		dbase.commit()
#		dbase.close()
		return True, r

def reject_an_auction_request(request_id, rejected_by_id):
	dbase = get_db()
	try:
		sql1 = f"UPDATE auction_requests SET approved = -1, response_by = {rejected_by_id} WHERE id = {request_id};"
		sql2 = f"DELETE FROM auction_list WHERE request_id = {request_id};"
		dbase.execute(sql1)
		dbase.execute(sql2)
	except sqlite3.IntegrityError:
#		dbase.close()
		return False
	except  TypeError:
#		dbase.close()
		return False
	else:
		dbase.commit()
#		dbase.close()
		return True

def get_auction_list():
	sql = "SELECT * FROM auction_list;"
	return get_db().execute(sql).fetchall()

def get_auction_details(auction_id):
	sql = "SELECT * FROM auction_list WHERE id = '{auction_id}';"
	return get_db().execute(sql).fetchone()


def get_auction_request(mode=AUCTION_REQUESTS_LIST_NOT_APPREVED):
	sql = "SELECT * FROM auction_requests WHERE approved=0 OR approved=1 OR approved=-1  ORDER BY approved ASC,id DESC;" if mode == AUCTION_REQUESTS_LIST_BOTH else f"SELECT * FROM auction_requests WHERE approved={mode} ORDER BY approved ASC,id DESC;"
	return get_db().execute(sql).fetchall();

def get_requests_list_by_id(uid, mode=AUCTION_REQUESTS_LIST_NOT_APPREVED):
	sql = f"SELECT * FROM auction_requests WHERE seller_id = '{uid}'  ORDER BY approved ASC,id DESC;" if mode == AUCTION_REQUESTS_LIST_BOTH else f"SELECT * FROM auction_requests WHERE seller_id = '{uid}',approved={mode} ORDER BY approved ASC,id DESC;"
	return get_db().execute(sql).fetchall();

def add_new_message(f, t, sub, msg):
	sql = f'INSERT INTO msg(msg_from, msg_to, msg_subject, msg_data) VALUES ({f}, {t}, {sub}, {msg});'
	dbase = get_db()
	dbase.execute(sql)
	dbase.commit()


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
	dbase = get_db()
	sql = f"UPDATE auction_list SET start_datetime = '{start_time}', end_datetime = '{end_time}', finalized = 1 WHERE id = {auction_id};"
	dbase.execute(sql)
	dbase.commit()

def status_auction(auction_id):
	dbase = get_db()
	sql = f"SELECT status FROM auction_list WHERE id = {auction_id};"
	return dbase.execute(sql).fetchone()

def cancel_auction(uid, auction_id):
	dbase = get_db()
	sql = f"UPDATE auction_list SET status = -2 WHERE id = {auction_id} AND seller_id = {uid};"
	dbase.execute(sql).fetchone()
	dbase.commit()
	return 1

def cancel_bid(participant_id, auction_id):
	sql = f"DELETE FROM bids WHERE participant_id = '{participant_id}' AND auction_id = '{auction_id}' ;"
	dbase = get_db()
	dbase.execute(sql)
	dbase.commit()

def make_bid(bidder_id, auction_id, qty, ppi, amt, finalPayment):
	sql1 = f"SELECT id FROM bids WHERE pariticipant_id = '{bidder_id}' AND auction_id = '{auction_id}' ;"
	dbase = get_db()
	r = dbase.execute(sql1).fetchone()
	if r is not None:
		sql2 = f"UPDATE bids SET qty = '{qty}', ppi= '{ppi}', amt = '{amt}', fPay = '{finalPayment}' WHERE id = '{r[0]}' ;"
		dbase.execute(sql2)
		commit()
		return r[0]
	sql3 = f"INSERT INTO bids (participant_id, auction_id, qty, ppi, amt, fPay) VALUES ('{bidder_id}', '{auction_id}', '{qty}', '{ppi}', '{amt}', '{finalPayment}');"
	r1 = dbase.execute(sql3)
	dbase.commit()
	return r1.lastrowid




