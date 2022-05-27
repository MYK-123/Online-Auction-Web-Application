#!/usr/bin/python3

import datetime
import logging
import requests

from flask import Blueprint
from flask import g
from flask import request
from flask import render_template

from src.connectivity import get_order_id
from src.connectivity import create_payment
from src.connectivity import getBidInfo
from src.connectivity import get_trans_list
from src.connectivity import get_trans_history

from src.auth import login_required

from src.constants import MERCHANT_ID
from src.constants import MERCHANT_KEY
from src.constants import WEBSITE_NAME
from src.constants import INDUSTRY_TYPE_ID
from src.constants import CHANNEL_ID
from src.constants import BASE_URL

from src.payment.paytm_checksum import generate_checksum
from src.payment.paytm_checksum import verify_checksum


bp = Blueprint('payments', __name__)

logging.basicConfig(level=logging.DEBUG)


@bp.route("/transaction/history/")
@login_required
def trans_history():
	return render_template('payment_list.html',heading='Transaction History' , items=get_trans_history(), name = g.user.get_username(), role=g.user.get_role())


@bp.route("/payments/checkout/")
@login_required
def payment_list():
	return render_template('payment_list.html',heading='Payments', items=get_trans_list(), name = g.user.get_username(), role=g.user.get_role())


@bp.route('/payments/<int:auction_id>/<int:bid_id>/checkout/', methods=['GET', 'POST'])
@login_required
def pay_proceed(auction_id, bid_id):
	order_id = get_order_id(auction_id, bid_id)
	if order_id == None:
		return redirect(request.url)
	bid_info = getBidInfo(bid_id)
	qty = bid_info.getQuantity()
	ppi = bid_info.getPricePerItem()
	fpay = bid_info.getFPay()
	amount = bid_info.getAmount()
	customer_id = "CUST_" + str(g.user.get_uid())
	
	display_data = {
		"ORDER_ID ": order_id,
		"Amount ": amount,
		"MOBILE NO ": str(7777777778),
		"E-MAIL ": "alpha@beta.gamma"
	}
	
	transaction_data = {
		"MID": MERCHANT_ID,
		"WEBSITE": WEBSITE_NAME,
		"INDUSTRY_TYPE_ID": INDUSTRY_TYPE_ID,
		"ORDER_ID": order_id,#str(datetime.datetime.now().timestamp()),
		"CUST_ID": customer_id,
		"TXN_AMOUNT": str(amount),
		"CHANNEL_ID": "WEB",
		"MOBILE_NO": "7777777777",
		"EMAIL": "example@paytm.com",
		"CALLBACK_URL": "http://localhost/payments/callback"
	}
	
	# Generate checksum hash
	transaction_data["CHECKSUMHASH"] = generate_checksum(transaction_data, MERCHANT_KEY)
	
	logging.info("Request params: {transaction_data}".format(transaction_data=transaction_data))
	
	url = BASE_URL + '/theia/processTransaction'
	return render_template("payment_proceed.html",display=display_data, data=transaction_data, url=url, name=g.user.get_username(), role=g.user.get_role())


@bp.route('/payments/callback/', methods=['GET', 'POST'])
@login_required
def callback():
	# log the callback response payload returned:
	callback_response = request.form.to_dict()
	logging.info("Transaction response: {callback_response}".format(callback_response=callback_response))
	
	# verify callback response checksum:
	checksum_verification_status = verify_checksum(callback_response, MERCHANT_KEY, callback_response.get("CHECKSUMHASH"))
	logging.info("checksum_verification_status: {check_status}".format(check_status=checksum_verification_status))
	
	# verify transaction status:
	transaction_verify_payload = {
		"MID": callback_response.get("MID"),
		"ORDERID": callback_response.get("ORDERID"),
		"CHECKSUMHASH": callback_response.get("CHECKSUMHASH")
	}
	url = BASE_URL + '/order/status'
	verification_response = requests.post(url=url, json=transaction_verify_payload)
	
	logging.info("Verification response: {verification_response}".format(
	verification_response=verification_response.json()))
	
	return render_template("payment_callback.html", callback_response=callback_response, checksum_verification_status=checksum_verification_status, verification_response=verification_response.json(), name=g.user.get_username(), role=g.user.get_role())








