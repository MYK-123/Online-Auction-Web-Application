#!/usr/bin/python3

from flask import g
from flask import Blueprint
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template

from src.connectivity import make_bid
from src.connectivity import cancel_bid
from src.connectivity import get_auction_details

bp = Blueprint('participate', __name__)

def finalP(amt):
	charges = (5 / 100) * amt #  5% of amt
	famt = amt - charges
	return famt


@bp.route('/participate/<int:auction_id>/', methods=['GET', 'POST'])
def bid(auction_id):
	bidder_id = g.user.get_uid()
	auction_details = get_auction_details(auction_id)
	if request.method == 'POST':
		qty = request.form['qty']
		ppi = request.form['ppi']
		amt = request.form['amt']
		bid_id = make_bid(bidder_id, auction_id, qty, ppi, amt, finalP(amt))
		return render_template('participate.html', qty=qty, ppi=ppi, amt=amt, details=auction_details, name=g.user.get_username())
	return render_template('participate.html', details=auction_details, name=g.user.get_username())

@bp.route('/participate/<int:auction_id>/bid/', methods=['GET', 'POST'])
def cancel_bid(auction_id):
	cancel_bid(g.user.get_uid(), auction_id)
	return redirect(url_for('participate.bid'))



