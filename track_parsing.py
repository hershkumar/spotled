import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import time

# defines the track class
# we pass in the output of the spotify call, and it'll parse the meaningful data out of it
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
		return self.track_obj.get('is_playing')

	def get_track_id(self):
		return self.track_obj.get('item').get('id')

# load the client keys from a file
secrets = open("keys.txt", "r")
CLIENT_ID = secrets.readline().strip()
CLIENT_SECRET = secrets.readline().strip()
REDIRECT_URI = secrets.readline().strip()

# What we want to access
scope = "user-read-currently-playing"

# do the authentication voodoo
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

printer = pprint.PrettyPrinter()
# poll to get the track that is currently playing
curr_track = track(sp.current_user_playing_track())
if (not curr_track.track_obj == None):
	# access the stored data to get the necessary info
	print(curr_track.get_track_name() + " by " + curr_track.get_track_artist() + " on the album " + curr_track.get_track_album_name() + ", song id: " + str(curr_track.get_track_id()))

	# Now we want to access the numerical data for a track
	features = sp.audio_features(curr_track.get_track_id())[0]
