#!/usr/bin/bash

export FLASK_APP=src/app
export FLASK_DEBUG=True


flask init_db
flask run

