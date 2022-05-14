
from src.app import return_app

if __name__ == '__main__':
	return_app().run(host='0.0.0.0', port=80, debug=True)
