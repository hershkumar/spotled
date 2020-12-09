import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request
from flask_session import Session
from colour import Color
import sqlite3
import datetime

try:
	import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
	import fake_rpigpio.utils
	fake_rpigpio.utils.install()
	import enum
	import math
	from threading import Thread
	from time import sleep

	class LedColor():
		h_val, s_val, v_val = 0, 0, 0

		def rgb_to_hsv(self, r, g, b):
			rgb_values = [r/255.0, g/255.0, b/255.0]
			conversion_constants = [((rgb_values[1] - rgb_values[2]), 360), 
			((rgb_values[2] - rgb_values[0]), 120),
			((rgb_values[0] - rgb_values[1]), 240)]

			max_color_index = rgb_values.index(max(rgb_values)) 
			min_color_index = rgb_values.index(min(rgb_values))
			diff = rgb_values[max_color_index] - rgb_values[min_color_index] 

			if rgb_values[max_color_index] == rgb_values[min_color_index]:
				h_val = 0
			else:
				h_val = (60 * (conversion_constants[max_color_index][0] / diff) + conversion_constants[max_color_index][1]) % 360

				if rgb_values[max_color_index] == 0:
					s_val = 0
				else:
					s_val = (diff / rgb_values[max_color_index]) * 100
					
					v_val = rgb_values[max_color_index] * 100

					return (round(h_val), round(s_val), round(v_val))

    #this is broken dont use it yet
    def hsv_to_rgb(self):
    	h_val, s_val, v_val = self.h_val, self.s_val/100., self.v_val/100.
    	i = math.floor((h_val) * 6)
    	f = h_val * 6 - i
    	p = v_val * (1 - s_val)
    	q = v_val * (1 - f * s_val)
    	t = v_val * (1 - (1 - f) * s_val)

    	rgb_combos = [(v_val, t, p), 
    	(q, v_val, p), 
    	(p, v_val, t), 
    	(p, q, v_val), 
    	(t, p, v_val), 
    	(v_val, p, q)]

    	rgb_val = rgb_combos[i % 6]
    	return (round(rgb_val[0] * 255), 
    		round(rgb_val[1] * 255), 
    		round(rgb_val[2] * 255))

    	class LedMode(enum.Enum):
    #function of brightness over time as a lambda
    STATIC = lambda brightness: brightness,
    BEATHING = lambda brightness: ()

    class LedDriver(Thread):

    UPDATE_RATE = 1 / 30 #hz

    def __init__(self, R_CHANNEL, G_CHANNEL, B_CHANNEL):
    	self.current_mode = LedMode.STATIC

    	RPi.GPIO.setmode(RPi.GPIO.BOARD)
    	RPi.GPIO.setup(R_CHANNEL, RPi.GPIO.OUT)
    	RPi.GPIO.setup(G_CHANNEL, RPi.GPIO.OUT)
    	RPi.GPIO.setup(B_CHANNEL, RPi.GPIO.OUT)

    	self.R_PWM = RPi.GPIO.PWM(R_CHANNEL, 100)
    	self.G_PWM = RPi.GPIO.PWM(G_CHANNEL, 100)
    	self.B_PWM = RPi.GPIO.PWM(B_CHANNEL, 100)

    	self.R_PWM.start(0)
    	self.G_PWM.start(0)
    	self.B_PWM.start(0)
    	
    	def set_rgb_power(self, rgb_vals):
    		self.R_PWM.ChangeDutyCycle(rgb_vals[0]/255.)
    		self.G_PWM.ChangeDutyCycle(rgb_vals[1]/255.)
    		self.B_PWM.ChangeDutyCycle(rgb_vals[2]/255.) 

    		def change_mode(self, new_mode):
    			self.current_mode = new_mode

    # def __run__(self):
    #     while True:
    #         if self.current_mode is not LedMode.STATIC:            
    #             for brightness in range(0, 101):
                    #todo: something eventually
    #     RPi.GPIO.cleanup()
    
# load the client keys from a file
secrets = open("keys.txt", "r")
CLIENT_ID = secrets.readline().strip()
CLIENT_SECRET = secrets.readline().strip()
REDIRECT_URI = secrets.readline().strip()

# What we want to access
scope = "user-read-currently-playing"

# do the authentication voodoo
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))
# get the username
username = sp.me().get('display_name')

ON = True
# how often the webpage should refresh itself, polling rate
global ref_rate
ref_rate = 30

# access the LEDs



class track:
	def __init__(self, track_obj):
		self.track_obj = track_obj

		def get_track_artist(self):
			return self.track_obj.get('item').get('artists')[0].get('name')

			def get_track_album_name(self):
				return self.track_obj.get('item').get('album').get('name')

				def get_track_name(self):
					return self.track_obj.get('item').get('name')

					def get_track_duration(self):
						return self.track_obj.get('item').get('duration_ms')

						def get_track_progress(self):
							return self.track_obj.get('progress_ms')

							def is_paused(self):
								return not self.track_obj.get('is_playing')

								def get_track_id(self):
									return self.track_obj.get('item').get('id')

									def get_color(features):
										energy = features.get('energy')
										valence = features.get('valence')
	# do some math here to get a single int between 0 and 100
	final = round((energy * 100 + (1 - valence) * 50)/2)
	final = round(energy * 100)
	# make a color gradient
	colors = list(Color("blue").range_to(Color("red"), 101))
	return colors[final]

	def insert_track_into_db(db, curr_track, features):
		db.execute("INSERT INTO TRACKS (ID, NAME, ARTIST, ALBUM, ENERGY, VALENCE, LOUDNESS, TEMPO)\
			VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (curr_track.get_track_id(), curr_track.get_track_name(), curr_track.get_track_artist(), curr_track.get_track_album_name(), float(features.get('energy')), float(features.get('valence')), float(features.get('loudness')), float(features.get('tempo'))))
		print("added song to db")

		def check_in_db(db, curr_track):
	# make a cursor for the db
	curs = db.cursor()
	curs.execute("SELECT * FROM TRACKS WHERE ID=?", (curr_track.get_track_id(),))
	ret = curs.fetchall()
	return ret

	def clear_db(db):
		db.execute("DELETE FROM TRACKS")

#create the flask object
app = Flask(__name__)

# default routing
@app.route('/')
@app.route('/index')
def index():
	# if the system is on
	if (ON):
		# connect to the sqlite3 database
		db = sqlite3.connect('tracks.db', isolation_level=None)
		print("connected to the database")
		# get the user's currently playing track
		curr_track = track(sp.current_user_playing_track())
		# check whether they're actually playing something on spotify
		if (curr_track.track_obj == None):
			return "You are not playing any music on Spotify"
		else:
			check = check_in_db(db, curr_track)
			user = {'username': username}
			song = {'energy': None, 'valence': None, 'loudness': None, 'tempo': None, 'color': 'white'}
			# if the song isn't paused
			if (curr_track.track_obj != None or (not curr_track.is_paused())):
				user = {'username': username, 'curr_track_name': curr_track.get_track_name(), 'curr_track_artist': curr_track.get_track_artist(), 'curr_track_album' : curr_track.get_track_album_name()}
				# if the song is in the db, we dont need to do this
				if (len(check) == 0):
					features = sp.audio_features(curr_track.get_track_id())[0]
					insert_track_into_db(db, curr_track, features)
				else:
					#otherwise just get it from the db
					features = {
					'energy': check[0][4],
					'valence': check[0][5],
					'loudness': check[0][6],
					'tempo': check[0][7],
					}
					song = {'energy' : features.get('energy'), 'valence' : features.get('valence'),'loudness' : features.get('loudness'), 'tempo' : features.get('tempo'), 'color': get_color(features)}
					timestamp = datetime.datetime.now()
					return render_template('index.html', user=user, song=song, time=timestamp, refresh=ref_rate)
				else:
					return "The system is currently off."


					@app.route('/settings')
					def settings_page():
						return render_template('settings.html')

						@app.route('/settings', methods=['POST'])
						def settings_post():
							global ref_rate
							
							new_rate = int(request.form['ref_rate'])
							if (isinstance(new_rate, int)):
								ref_rate = new_rate
								return render_template('settings.html')
							else:
								return render_template('settings.html')

								if __name__ == '__main__':
									app.run(host='0.0.0.0', threaded=True, debug=True)