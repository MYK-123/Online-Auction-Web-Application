#!/usr/bin/python3

from flask import Blueprint

bp = Blueprint('participate', __name__)

@bp.route('/participate/<int:auction_id>/', methods=['GET', 'POST'])
def participate(auction_id):
	return b'PARTICIPATE'

@bp.route('/participate/<int:auction_id>/bid/', methods=['GET', 'POST'])
def bid(auction_id):
	return b'PARTICIPATE'

@bp.route('/participate/<int:auction_id>/bid/', methods=['GET', 'POST'])
def cancel_bid(auction_id):
	return b'PARTICIPATE'

