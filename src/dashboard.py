#!/usr/bin/python3

import os
from src.constants import UPLOAD_FOLDER
from src.auth import login_required
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import send_from_directory

from flask.blueprints import Blueprint

from jinja2 import Markup

from werkzeug.utils import secure_filename

from src.connectivity import create_auction_requst
from src.connectivity import get_auctions_list
from src.connectivity import get_requests_list_by_id_both


bp = Blueprint('dashboard', __name__)

def get_auction_table():
	msg = get_auctions_list()
	l = []
	button_format = "<input type='image' src='/static/img/participate.png' formaction='/participate/{auction_id}/' />"
	for i in msg:
		item = []
		for key in i.keys():
			item.append(i[key])
		item.append(button_format.format(auction_id=i['id']))
		l.append(item)
	return l

@bp.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
	r = session.get('user_id')
	l = get_auction_table()
	return Markup.unescape(render_template('dashboard.html', name=r, items=l, rowname='t2'))


@bp.route('/sell/', methods=['GET', 'POST'])
@login_required
def sell():
	user_id = session.get('user_id')
	if request.method == 'POST':
		req_id = create_auction_requst(user_id, request.form['title'], request.form['desc'], request.form['qty'], request.form['price'])
		if 'attachments' not in request.files:
			flash('No File part')
			return redirect(request.url)
		for file in request.files.getlist('attachments'):
			if file.filename != '':
				save_uploaded_files(file, user_id, str(req_id))
		return redirect(url_for('dashboard.dashboard'))
	return render_template('sell.html', name=user_id)

def save_uploaded_files(file,user_id, req_id):
	filename = secure_filename(file.filename)
	path = os.path.join(os.path.join(UPLOAD_FOLDER, user_id), req_id)
	os.makedirs(path, exist_ok=True)
	file.save(os.path.join(path, filename))

@bp.route('/requests/status/', methods=['GET', 'POST'])
@login_required
def sell_status_user():
	uid = session.get('user_id')
	l = get_requests_list_by_id_both(uid)
	return render_template('auction_requests.html', items=l, name=uid, rowname='t2')

@bp.route('/requests/<int:req_id>/status/', methods=['GET', 'POST'])
@login_required
def sell_status(req_id):
	uid = session.get('user_id')
	l = get_requests_list_by_id_both(uid)
	row = []
	for i in l:
		if i['id'] == req_id:
			row.append(i)
	return render_template('auction_requests.html', items=row, name=uid, rowname='t2')

