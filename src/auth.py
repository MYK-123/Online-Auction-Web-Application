#!/usr/bin/python3

import functools

from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import current_app
from flask import g

from flask.blueprints import Blueprint

from src.connectivity import check_password
from src.connectivity import create_account
from src.connectivity import get_user_id
from src.connectivity import validate_username
from src.connectivity import fetch_security_question
from src.connectivity import validate_security_answer
from src.connectivity import update_password
from src.connectivity import get_role
from src.connectivity import getuser

bp = Blueprint('auth', __name__)

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kargs):
		if session.get('username') is None:
			return redirect(url_for('auth.login'))
		return view(**kargs)
	return wrapped_view


@bp.route('/auth/register/', methods=["POST", "GET"])
def register():
	if session.get('username'):
		return redirect(url_for('dashboard.dashboard'))
	info = ''
	if request.method == "POST":
		fn = request.form['fname']
		ln = request.form['lname']
		un = request.form['username']
		pan = request.form['panno']
		password = request.form['password']
		confpass = request.form['confpass']
		secq = request.form['secques']
		seca = request.form['secans']
		if password == confpass:
			r = create_account(fn, ln, un, pan, password, secq, seca)
			if r:
				g.user = getuser(un)
				session['username'] = g.user.get_username()
				return redirect(url_for('dashboard.dashboard'))
			else:
				info += 'cannot create account due to some error occured'
		else:
			info += "passwords doesn't match"
	return render_template('register.html', msg=info)


@bp.route('/auth/login/', methods=["GET", "POST"])
def login():
	if session.get('username'):
		return redirect(url_for('dashboard.dashboard'))
	if request.method == "POST":
		return do_login(request.form['username'], request.form['password'])
	return render_template('login.html')

def do_login(username, password):
	if check_password(username, password):
		g.user = getuser(username)
		session['username'] = g.user.get_username()
		return redirect(url_for('dashboard.dashboard'))
	return render_template('login.html', recover='recover')

@bp.route('/auth/recover/', methods=['GET', 'POST'])
def recover():
	error = ''
	if request.method == 'POST':
		username = request.form['username']
		if validate_username(username):
			secq = fetch_security_question(username)
			return render_template('recover.html', username=username, secq=secq)
		else:
			error = 'User does not exist'
	return render_template('recover.html', msg=error)

@bp.route('/auth/recover/<username>/answer', methods=['POST'])
def recover1(username):
	error = ''
	if validate_username(username):
		secq = fetch_security_question(username)
		seca = request.form['seca']
		if not validate_security_answer(username, seca):
			seca = None
			error = 'Answers do not match'
		return render_template('recover.html', username=username, secq=secq, seca=seca, msg=error)
	else:
		error = 'User does not exist'
	return render_template('recover.html', msg=error)

@bp.route('/auth/recover/<username>/answer/pass', methods=['POST'])
def recover2(username):
	error = ''
	if validate_username(username):
		secq = fetch_security_question(username)
		seca = request.form['seca']
		if validate_security_answer(username, seca):
			pass1 = request.form['newp']
			pass2 = request.form['confp']
			if pass1 == pass2:
				if update_password(username, pass1):
					return redirect(url_for('auth.login'))
				else:
					error = 'Cannot update password due to some unknown error occured'
			else:
				error = 'passwords do not match'
		return render_template('recover.html', username=username, secq=secq, seca=seca, msg=error)
	else:
		error = 'User does not exist'
	return render_template('recover.html', msg=error)



@bp.route('/auth/logout', methods=['GET', 'POST'])
def logout():
	session.clear()
	return redirect(url_for('home'))

