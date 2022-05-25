#!/usr/bin/python3

import functools

from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask.blueprints import Blueprint

from jinja2 import Markup

from src.auth import login_required

from src.messages import send_approval_message
from src.messages import send_rejection_message

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
from src.connectivity import get_users_list



bp = Blueprint('internals', __name__)

def is_admin(view):
	@functools.wraps(view)
	def wrapped_view(**kargs):
		if g.user.get_role() != USER_ROLE_ADMIN:
			return redirect(url_for('home'))
		return view(**kargs)
	return wrapped_view

def is_manager(view):
	@functools.wraps(view)
	def wrapped_view(**kargs):
		if g.user.get_role() != USER_ROLE_MANAGER and g.user.get_role() != USER_ROLE_ADMIN:
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

@bp.route('/requests/approve/<int:req_id>/<int:user_id>/', methods=['POST'])
@is_manager
@login_required
def req_approve(req_id, user_id):
	auction_id = approve_req(req_id, user_id)
	if auction_id is None:
		return redirect(url_for('.auction_requests'))
	send_approval_message(auction_id, req_id)
	return redirect(url_for('.auction_requests'))

@bp.route('/requests/reject/<int:req_id>/<int:user_id>/', methods=['POST'])
@is_manager
@login_required
def req_reject(req_id, user_id):
	auction_id = reject_req(req_id, user_id)
	if auction_id is None:
		return redirect(url_for('.auction_requests'))
	send_rejection_message(auction_id, req_id)
	return redirect(url_for('.auction_requests'))


@bp.route('/requests/', methods=['GET', 'POST'])
@login_required
@is_manager
def auction_requests():
	r = g.user.get_username()
	l = get_auction_requests_both()
	return Markup.unescape(render_template('auction_requests.html', name=r, uid=g.user.get_uid(), items=l, rowname='t2', staff='true',role=g.user.get_role()))


@bp.route('/admin/add/<int:admin_id>/', methods=['GET','POST'])
@login_required
@is_admin
def add_admin(admin_id):
	r = make_administrator(admin_id)
	return redirect(url_for('.admin_controls'))

@bp.route('/manager/add/<int:manager_id>/', methods=['GET','POST'])
@login_required
@is_admin
def add_manager(manager_id):
	r = make_manager(manager_id)
	return redirect(url_for('.admin_controls'))

@bp.route('/admin/remove/<int:user_id>/', methods=['GET','POST'])
@bp.route('/manager/remove/<int:user_id>/', methods=['GET','POST'])
@login_required
@is_admin
def normal_user(user_id):
	r = make_normal_user(user_id)
	return redirect(url_for('.admin_controls'))

@bp.route('/admin/add/', methods=['GET','POST'])
@bp.route('/admin/remove/', methods=['GET','POST'])
@bp.route('/manager/add/', methods=['GET','POST'])
@bp.route('/manager/remove/', methods=['GET','POST'])
@login_required
@is_admin
def admin_controls():
	return render_template('role_change.html', rowname='t2', name=g.user.get_username(), items=get_users_list(),role=g.user.get_role())

