@echo off

set FLASK_APP=src/app

python -m pytest tests
