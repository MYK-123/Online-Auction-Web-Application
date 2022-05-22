	
import pytest
from flask import g, session
from src.connectivity.db import get_db


def test_register(client, auth, app):
	assert client.get('/auth/register/').status_code == 200
	response = auth.register('a','a')
	assert '/dashboard/' in response.location
	auth.logout()
	with app.app_context():
		assert get_db().execute(
		"SELECT * FROM user WHERE username = 'a'"
		).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
	('', '', b'Redirecting'),
	('a', '', b'Redirecting'),
	('test', 'test', b'Redirecting')
))
def test_register_validate_input(auth, username, password, message):
	response = auth.register(username, password)
	auth.logout()
	assert message in response.data

def test_login(client, auth):
	assert client.get('/auth/login/').status_code == 200
	auth.register()
	auth.logout()
	response = auth.login()
	response = auth.login()
	print(response.location)
	assert '/dashboard/' in response.location
	
	with client:
		client.get('/')
		assert session.get('username') != None


@pytest.mark.parametrize(('username', 'password', 'message'), (
	('a', 'test', b'Forgot Password'),
	('test', 'b', b'Forgot Password')
))
def test_login_validate_input(auth, username, password, message):
	response = auth.login(username, password)
	assert message in response.data


def test_logout(client, auth):
	auth.login()
	
	with client:
		auth.logout()
		assert 'user_id' not in session


