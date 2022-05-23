#!/usr/bin/python3

from flask import Blueprint

bp = Blueprint('bot', __name__)

@bp.route('/alg/start/', methods=['GET', 'POST'])
def start():
	pass

@bp.route('/alg/stop/', methods=['GET', 'POST'])
def stop():
	pass

