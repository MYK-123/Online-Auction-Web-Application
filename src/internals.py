#!/usr/bin/python3

import functools

from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

from flask.blueprints import Blueprint

from jinja2 import Markup

from src.auth import login_required
from src.constants import USER_ROLE_ADMIN
from src.constants import USER_ROLE_MANAGER

from src.connectivity import approve_auction_id
from src.connectivity import reject_auction_id
from src.connectivity import get_auction_requests_approved
from src.connectivity import get_auction_requests_unapproved
from src.connectivity import get_auction_requests_both
from src.connectivity import make_manager
from src.connectivity import make_administrator
from src.connectivity import make_normal_user



bp = Blueprint('internals', __name__)

def is_admin(view):
	@functools.wraps(view)
	def wrapped_view(**kargs):
		if session.get('role') != USER_ROLE_ADMIN:
			return redirect(url_for('home'))
		return view(**kargs)
	return wrapped_view

def is_manager(view):
	@functools.wraps(view)
	def wrapped_view(**kargs):
		if session.get('role') != USER_ROLE_MANAGER and session.get('role') != USER_ROLE_ADMIN:
			return redirect(url_for('home'))
		return view(**kargs)
	return wrapped_view


def approve_req(req_id, approved_by):
	r = approve_auction_id(req_id, approved_by)
	if r == -1:
		return None
	return r

def reject_req(req_id, rejected_by):
	r = reject_auction_id(req_id, rejected_by)
	if r == -1:
		return None
	return r

@bp.route('/requests/approve/<int:req_id>/<int:user_id>/', methods=['GET', 'POST'])
@is_manager
@login_required
def req_approve(req_id, user_id):
	auction_id = approve_req(req_id, user_id)
	if auction_id is None:
		return redirect(url_for('.auction_requests'))
#	send_approval_message(auction_id)
	return redirect(url_for('.auction_requests'))

@bp.route('/requests/reject/<int:req_id>/<int:user_id>/', methods=['GET', 'POST'])
@is_manager
@login_required
def req_reject(req_id, user_id):
	auction_id = reject_req(req_id, user_id)
	if auction_id is None:
		return redirect(url_for('.auction_requests'))
#	send_approval_message(auction_id)
	return redirect(url_for('.auction_requests'))

def get_request_table(f, user_id):
	msg = f()
	l = []
	button_format = "<input type='image' src='/static/img/appreve.png' alt='Reject Request' formaction='/requests/reject/{req_id}/{user_id}/' /><input type='image' src='/static/img/appreve.png' alt='Approve Request' formaction='/requests/approve/{req_id}/{user_id}/' />"
	for i in msg:
		item = []
		for key in i.keys():
			item.append(i[key])
		item.append(button_format.format(req_id=i['id'], user_id=user_id))
		l.append(item)
	return l

@bp.route('/requests/', methods=['GET', 'POST'])
@login_required
@is_manager
def auction_requests():
	r = session.get('user_id')
	l = get_request_table(get_auction_requests_both, r)
	return Markup.unescape(render_template('auction_requests.html', name=r, items=l, rowname='t2'))


@bp.route('/admin/add/<int:admin_id>/', methods=['GET','POST'])
@login_required
@is_admin
def add_admin(admin_id):
	r = make_administrator(admin_id)
	return "ADMIN ADDED"

@bp.route('/manager/add/<int:manager_id>/', methods=['GET','POST'])
@login_required
@is_admin
def add_manager(manager_id):
	r = make_manager(manager_id)
	return "MANAGER ADDED"

@bp.route('/admin/remove/<int:user_id>/', methods=['GET','POST'])
@bp.route('/manager/remove/<int:user_id>/', methods=['GET','POST'])
@login_required
@is_admin
def normal_user(user_id):
	r = make_normal_user(user_id)
	return "USER SET TO NORMAL USER"

