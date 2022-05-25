 #!/usr/bin/python3

import os

from flask import g
from flask import Blueprint
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template

from src.auth import login_required

from src.constants import UPLOAD_FOLDER

from src.connectivity import make_bid
from src.connectivity import cancel_bid
from src.connectivity import get_auction_details
from src.connectivity import get_auctions_list

bp = Blueprint('participate', __name__)

def finalP(amt):
	charges = (5 / 100) * amt #  5% of amt
	famt = amt - charges
	return famt

def get_files(auction_id):
	l = []
	req_id = get_auction_details(auction_id)['request_id']
	user_id = g.user.get_uid()
	path = os.path.join(os.path.join(UPLOAD_FOLDER, str(user_id)), str(req_id))
	for i, f in enumerate(os.list_dir(path)):
		x = []
		x.append(i)
		x.append(f)
		l.append(x)
	return l


@bp.route('/participate/', methods=['GET', 'POST'])
@login_required
def participate():
	return render_template('participate_1.html', name=g.user.get_username(), items=get_auctions_list())


@bp.route('/participate/<int:auction_id>/', methods=['GET', 'POST'])
@login_required
def bid(auction_id):
	bidder_id = g.user.get_uid()
	auction_details = get_auction_details(auction_id)
	if request.method == 'POST':
		qty = request.form['qty']
		ppi = request.form['price']
		amt = request.form['amt']
		bid_id = make_bid(bidder_id, auction_id, qty, ppi, amt, finalP(amt))
		return render_template('participate.html', qty=qty, ppi=ppi, amt=amt, auction=auction_details, name=g.user.get_username(), files=get_files(auction_id))
	return render_template('participate.html', auction=auction_details, name=g.user.get_username(), files=get_files(auction_id))

@bp.route('/participate/<int:auction_id>/cancel_bid/', methods=['GET', 'POST'])
@login_required
def cancel_bid(auction_id):
	cancel_bid(g.user.get_uid(), auction_id)
	return redirect(url_for('participate.bid'))



