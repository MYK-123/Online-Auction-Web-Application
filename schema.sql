CREATE TABLE IF NOT EXISTS user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	fname TEXT,
	lname TEXT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	pan_no TEXT UNIQUE,
	secques TEXT,
	secans TEXT,
	address TEXT,
	role TEXT DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS auction_requests(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	seller_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT,
	description TEXT,
	quantity INTEGER NOT NULL DEFAULT 1,
	min_price FLOAT NOT NULL DEFAULT 0 CHECK(min_price >= 0),
	approved INTEGER NOT NULL DEFAULT 0 CHECK(approved == 0 OR approved == 1 OR approved == -1),
	response_by INTEGER,

	FOREIGN KEY(seller_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS auction_list(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	seller_id INTEGER NOT NULL,
	request_id INTEGER UNIQUE NOT NULL,
	created TIMESTAMP NOT NULL,
	approved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	approved_by INTEGER NOT NULL,
	title TEXT,
	description TEXT,
	quantity INTEGER NOT NULL DEFAULT 1,
	min_price FLOAT NOT NULL,
	start_datetime TIMESTAMP,
	end_datetime TIMESTAMP,
	finalized INTEGER NOT NULL DEFAULT 0 CHECK(finalized == 0 OR finalized == 1),
	status INTEGER DEFAULT 0 CHECK(status == 0 OR status == 1 OR status == -1 OR status == -2),
	
	FOREIGN KEY("request_id") REFERENCES "auction_requests"("id"),
	FOREIGN KEY("approved_by") REFERENCES "user"("id"),
	FOREIGN KEY("seller_id") REFERENCES "user"("id")
);

CREATE TABLE IF NOT EXISTS msg(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	msg_from INTEGER NOT NULL,
	msg_to INTEGER NOT NULL,
	msg_subject TEXT,
	msg_data TEXT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bids (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	participant_id INTEGER NOT NULL,
	auction_id INTEGER NOT NULL,
	qty INTEGER,
	ppi FLOAT,
	amt FLOAT,
	fPay FLOAT,
	msg_sent TEXT DEFAULT '',
	
	FOREIGN KEY("participant_id") REFERENCES "user"("id"),
	FOREIGN KEY("auction_id") REFERENCES "auction_list"("id")
);

CREATE TABLE IF NOT EXISTS trans (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	trans_id TEXT,
	order_id TEXT UNIQUE NOT NULL,
	bid_id INTEGER NOT NULL,
	auction_id INTEGER NOT NULL,
	qty INTEGER,
	ppi FLOAT,
	amt FLOAT,
	bidder_paid TEXT DEFAULT 'NOT PAID',
	seller_order_id TEXT,
	seller_trans_id TEXT,
	seller_paid TEXT DEFAULT 'NOT PAID',
	seller_Pay FLOAT,
	init_time TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
	
	FOREIGN KEY("bid_id") REFERENCES "bids"("id"),
	FOREIGN KEY("auction_id") REFERENCES "auction_list"("id")
	
);

