import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask
from flask_session import Session
import uuid

# load the client keys from a file
secrets = open("keys.txt", "r")
CLIENT_ID = secrets.readline().strip()
CLIENT_SECRET = secrets.readline().strip()
REDIRECT_URI = secrets.readline().strip()

# What we want to access
scope = "user-read-currently-playing"

# do the authentication voodoo
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

#create the flask object
app = Flask(__name__)

# default routing
@app.route('/')
def index():
	return 'Hello World!'


@app.route('/settings')
def settings_page():
	return 'Settings will go here'

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)