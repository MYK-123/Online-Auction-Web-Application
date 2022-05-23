#!/usr/bin/python3

from flask import Blueprint
from flask import g
from flask import render_template

from src.connectivity import generate_order_id
from src.connectivity import create_payment
from src.connectivity import getBidInfo

bp = Blueprint('payments', __name__)


@bp.route('/payments/<int:auction_id>/<int:bid_id>/checkout/', methods=['GET', 'POST'])
def make_payment(auction_id, bid_id):
	order_id = generate_order_id(auction_id, bid_id)
	bid_info = getBidInfo(bid_id)
	qty = bid_info.getQuantity()
	ppi = bid_info.getPricePerItem()
	amt = bid_info.getAmount()
	fpay = bid_info.getFpay()
	create_payment(order_id, bid_id, auction_id, qty, ppi, amt, fPay)
	return render_template('make_payment.html', name = g.user.get_username())



@bp.route('/payments/callback/', methods=['GET', 'POST'])
def payment_callback():
	pass

