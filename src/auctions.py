#!/usr/bin/python3

from flask import g
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint

from src.auth import login_required

from src.connectivity import get_auctions_list
from src.connectivity import save_auction_times
from src.connectivity import cancel_auction as cancel_auction1
from src.connectivity import status_auction
from src.connectivity import from_local_to_utc

bp = Blueprint('auctions', __name__)

@bp.route('/auctions/list/', methods=['GET', 'POST'])
@login_required
def list_auctions():
	uid = g.user.get_uid()
	lf = []
	for i in get_auctions_list():
		if i['seller_id'] == uid:
			lf.append(i)
	return render_template('auction_time_set.html', name=g.user.get_username(), items=lf, rowname='t2',role=g.user.get_role())


@bp.route('/auctions/<int:auction_id>/date/time/duration/confirm/', methods=['GET', 'POST'])
@login_required
def set_date_time_duration_of_auction(auction_id):
	if request.method == 'POST':
		date = request.form['date']
		stime = request.form['stime']
		etime = request.form['etime']
		tz = request.form['tz']
		start = date + ' ' + stime
		end = date + ' ' + etime
		start_utc = from_local_to_utc(start, tz, None)
		end_utc = from_local_to_utc(end, tz, None)
		save_auction_times(auction_id, start_utc, end_utc)
		return redirect(url_for('auctions.list_auctions'))
	uid = g.user.get_uid()
	lf = []
	for i in get_auctions_list():
		if i['seller_id'] == uid:
			lf.append(i)
	return render_template('auction_time_set.html', name=g.user.get_username(), items=lf, rowname='t2', set='true',role=g.user.get_role())


@bp.route('/auctions/<int:auction_id>/cancel/', methods=['GET', 'POST'])
@login_required
def cancel_auction(auction_id):
	uid = g.user.get_uid()
	ret = cancel_auction1(uid, auction_id)
	return jsonify(status=ret)


@bp.route('/auctions/<int:auction_id>/status/', methods=['GET', 'POST'])
def get_auction_status(auction_id):
	ret = status_auction(auction_id)
	return jsonify(status=ret[0])


