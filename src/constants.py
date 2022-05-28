#!/usr/bin/python3
import os

PROJECT_ROOT = '.'
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads/')
CONNECTIVITY_FOLDER = os.path.join(PROJECT_ROOT, 'connectivity')
SCHEMA_FILE = 'schema.sql'
DATABASE_FILE = 'database.db'
DATABASE_SCHEMA = os.path.join(CONNECTIVITY_FOLDER, SCHEMA_FILE)
DATABASE = os.path.join(CONNECTIVITY_FOLDER, DATABASE_FILE)

DATABASE_SCHEMA_FILE = DATABASE_SCHEMA

ALLOWED_EXTENTIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

AUCTION_REQUESTS_LIST_APPROVED = 1
AUCTION_REQUESTS_LIST_NOT_APPREVED = 0
AUCTION_REQUESTS_LIST_BOTH = 2

MESSAGE_KEY_TO = 'msg_to'
MESSAGE_KEY_FROM = 'msg_from'

USER_ROLE_ADMIN = 'admin'
USER_ROLE_MANAGER = 'manager'
USER_ROLE_USER = 'user'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

BOT_USERNAME = 'BOT'
BOT_PASSWORD = 'BOT'


# Staging configs:
# Keys from https://dashboard.paytm.com/next/apikeys
MERCHANT_ID = "YTGATi65911071937029"
MERCHANT_KEY = "8&iDNyJnLrn7#Sil"
WEBSITE_NAME = "WEBSTAGING"
INDUSTRY_TYPE_ID = "Retail"
CHANNEL_ID = "WEB"
BASE_URL = "https://securegw-stage.paytm.in"


# Production configs:
# Keys from https://dashboard.paytm.com/next/apikeys
#MERCHANT_ID = "<MERCHANT_ID>"
#MERCHANT_KEY = "<MERCHANT_KEY>"
#WEBSITE_NAME = "<WEBSITE_NAME>"
#INDUSTRY_TYPE_ID = "<INDUSTRY_TYPE_ID>"
#BASE_URL = "https://securegw.paytm.in"


