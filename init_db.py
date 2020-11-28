import sqlite3


db = sqlite3.connect('tracks.db')
print("connected to the database")

db.execute('''
	CREATE TABLE TRACKS (
	ID TEXT,
	NAME TEXT,
	ARTIST TEXT,
	ALBUM TEXT,
	ENERGY FLOAT,
	VALENCE FLOAT,
	LOUDNESS FLOAT,
	TEMPO FLOAT
	);
	''')
print("created table")