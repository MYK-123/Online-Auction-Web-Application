#!/usr/bin/python3

from flask import g
from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template

from src.auth import login_required

from src.connectivity import getuser
from src.connectivity import list_messages_to
from src.connectivity import list_messages_from
from src.connectivity import send_message
from src.connectivity import get_auction_requests_both

bp = Blueprint('messages', __name__)

@bp.route('/messages/send/', methods=['POST'])
@login_required
def send_msg():
	m_from = g.user.get_uid()
	m_to = getuser(request.get('to')).get_uid()
	m_sub = request.get('sub')
	m_data = request.get('data')
	send_message(m_from, m_to, m_sub, m_data)
	return redirect(request.url)


@bp.route('/messages/', methods=['GET', 'POST'])
@login_required
def get_messages():
	un = g.user.get_username()
	msg_to_l = list_messages_to(g.user.get_uid())
	return render_template('messages.html', name=g.user.get_username(), r=un, msglist=msg_to_l, role=g.user.get_role())


def send_approval_message(auction_id, req_id):
	l = get_auction_requests_both()
	seller_id = -1
	for i in l:
		if i['id'] == req_id:
			seller_id = i['seller_id']
	if seller_id == -1:
		return False
	f = g.user.get_uid()
	t = seller_id
	sub = "'System Notification'"
	data = f"""'Your Auction Request with request no {req_id} has been approved, and your generated auction id is {auction_id}.'"""
	send_message(f, t, sub, data)


def send_rejection_message(auction_id, req_id):
	l = get_auction_requests_both()
	seller_id = -1
	for i in l:
		if i['id'] == req_id:
			seller_id = i['seller_id']
	if seller_id == -1:
		return False
	f = g.user.get_uid()
	t = seller_id
	sub = "'System Notification'"
	data = f"""'Sorry, but your auction request with request no: {req_id} has been rejected.'"""
	send_message(f, t, sub, data)




