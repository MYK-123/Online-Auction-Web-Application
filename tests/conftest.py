
import os
import tempfile
import pytest

import sqlite3

from src.app import create_app
from src.connectivity.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
	_data_sql = f.read().decode('utf-8')

class AuthActions(object):
	def __init__(self, client):
		self._client = client
	
	def register(self, username='test', password='test', redirect=False):
		import random
		return self._client.post('/auth/register/', data={
			'fname':'test',
			'lname':'test',
			'username':username,
			'panno':random.random(),
			'password':password,
			'confpass':password,
			'secques':'test',
			'secans':'test'}, follow_redirects=False)
	
	def login(self, username='test', password='test', redirect=False):
		return self._client.post(
			'/auth/login/',
			data={'username':username, 'password':password},
			follow_redirects=redirect)
	
	def logout(self, redirect=False):
		self._client.get('/auth/logout/', follow_redirects=redirect)
	



@pytest.fixture
def app():
	db_fd, db_path = tempfile.mkstemp()
	
	app = create_app({
		'TESTING': True,
		'DATABASE': db_path
	})
	
	with app.app_context():
		init_db()
		get_db().executescript(_data_sql)
	
	yield app
	
	os.close(db_fd)
	os.unlink(db_path)

@pytest.fixture
def client(app):
	return app.test_client()

@pytest.fixture
def runner(app):
	return app.test_cli_runner()

@pytest.fixture
def auth(client):
	return AuthActions(client)

