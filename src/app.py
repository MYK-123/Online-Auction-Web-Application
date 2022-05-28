#!/usr/bin/python3

import os

from src.bot import start_bot
from src.connectivity import getuser

from src.constants import UPLOAD_FOLDER
from src.constants import DATABASE_FILE
from src.constants import DATABASE_SCHEMA_FILE

from flask import Flask
from flask import g
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from jinja2 import Markup

#import secrets

import src.auth as auth
import src.auctions as auctions
import src.dashboard as dashboard
import src.internals as internals
import src.messages as messages
import src.participate as participate
import src.payments as payments
import src.profile as profile



def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY = 'dbff3e78b2f405544565bea285c4c33ff656c7334ca75c4ce7f729e147ee4df8',
		DATABASE = os.path.join(app.instance_path, DATABASE_FILE)
	)
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.config['DATABASE_SCHEMA'] = DATABASE_SCHEMA_FILE
	
	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	#app.secret_key=secrets.token_hex()
	
	app.register_blueprint(auth.bp)
	app.register_blueprint(auctions.bp)
	app.register_blueprint(dashboard.bp)
	app.register_blueprint(internals.bp)
	app.register_blueprint(messages.bp)
	app.register_blueprint(participate.bp)
	app.register_blueprint(payments.bp)
	app.register_blueprint(profile.bp)

	
	@app.before_request
	def before_each_request():
		g.user = getuser(session.get('username'))
	
			
	@app.route('/')
	@app.route('/index')
	@app.route('/home')
	def home():
		if g.user:
			return redirect(url_for('dashboard.dashboard'))
		return Markup.unescape(render_template('index.html', items=dashboard.get_auction_table(), rowname='t2'))
	
	from src.connectivity import db
	db.init_app(app)
	
	start_bot(app.app_context())
	
	return app

def return_app():
	return create_app()
	


