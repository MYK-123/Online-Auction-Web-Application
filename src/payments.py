#!/usr/bin/python3

from flask import Blueprint

bp = Blueprint('payments', __name__)

@bp.route('/payments/checkout/', methods=['GET', 'POST'])
def make_payment():
	pass


@bp.route('/payments/callback/', methods=['GET', 'POST'])
def payment_callback():
	pass

