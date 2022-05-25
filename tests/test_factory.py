
from src.app import create_app

def test_config():
	assert not create_app().testing
	assert create_app({'TESTING':True}).testing

def test_home(client):
	response = client.get('/home')
	assert b'Home' in response.data

