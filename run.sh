#!/usr/bin/bash

export FLASK_APP=src/app
export FLASK_DEBUG=True
export FLASK_ENV=development
export FLASK_RUN_HOST=localhost
export FLASK_RUN_PORT=80


python3 -m flask init_db

python3 -m flask run

#flask init_db
#flask run

