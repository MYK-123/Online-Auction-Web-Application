
set FLASK_APP=src/app
set FLASK_DEBUG=True
set FLASK_ENV=development
set FLASK_RUN_HOST=localhost
set FLASK_RUN_PORT=80


python3 -m flask init_db

python3 -m flask run

