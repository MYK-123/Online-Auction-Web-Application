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
from src.connectivity import cancel_bida
from src.connectivity import get_auction_details
from src.connectivity import get_auctions_list

bp = Blueprint('participate', __name__)

def finalP(amt):
	charges = (5 / 100) * amt #  5% of amt
	famt = amt - charges
	return famt

def get_files(auction_id):
	l = []
	details = get_auction_details(auction_id)
	req_id = details['request_id']
	user_id = details['seller_id']
	path = os.path.join(os.path.join(UPLOAD_FOLDER, str(user_id)), str(req_id))
	if os.path.exists(path):
		for i, f in enumerate(os.listdir(path)):
			x = []
			x.append(i)
			path = os.path.join(os.path.join('/uploads/', str(user_id)), str(req_id))
			x.append(os.path.join(path, f))
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
		bid_id = make_bid(bidder_id, auction_id, qty, ppi, amt, finalP(int(amt)))
		return render_template('participate.html',role=g.user.get_role(), qty=qty, ppi=ppi, amt=amt, auction=auction_details, name=g.user.get_username(), files=get_files(auction_id))
	return render_template('participate.html', role=g.user.get_role(), auction=auction_details, name=g.user.get_username(), qty=auction_details['quantity'], price=auction_details['min_price'], files=get_files(auction_id))

@bp.route('/participate/<int:auction_id>/cancel_bid/', methods=['GET', 'POST'])
@login_required
def cancel_bid(auction_id):
	print("DELETE")
	cancel_bida(g.user.get_uid(), auction_id)
	return redirect(f"/participate/{auction_id}/")



