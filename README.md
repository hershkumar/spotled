# spotled
Making something that will interface with LED lights to change color based on what the user is listening to.

Plan:
- Get access to Spotify API
- Figure out how to query what a user is listening to
- Get a rating for how "heavy" the song is
- Use that to interface with the lights
- Set up a loop to change the color at certain intervals

Ideal features:
- Runs a webserver (Flask?)
	- Turns it off/on
	- Change users or something
	- hardcode genres to colors (or something idk)
	- Dim/brighten colors
- Updates within seconds of changing songs

### LED Interface

Server will be run on an RPI, probably gonna interface with the LEDs via gpio (Or ideally we have some wireless way of connecting to the lights from the rpi). GPIO isn't my ideal solution because thats kinda icky, but it might be the only option, seeing as that's what everyone on the internet seems to use.

Useful links:
https://dordnung.de/raspberrypi-ledstrip/

Seems to be basically 3 mosfets and a power adapter.

### Song Analysis
Spotify API gives us access to some audio features of a song:
- danceability
- energy
- loudness
- acousticness
- speechiness
- instrumentalness
- liveness
- valence
- tempo

Current plan is to use the energy and valence of the song to associate it with an emotion, and then apply this to a color gradient (ex. happy to sad maps from blue to red). This will give us a default color for every song. Another possibility is to change the brightness of the lights based on the loudness of the song.

#### Neural Net
The neural net will map the numerics given by spotify (the audio features above) and will map the numbers to a single value. The current plan is to make a playlist of a hundred-ish songs and manually rate the intensity of each song, and use that as a base set for training data (https://open.spotify.com/playlist/5rkJQBt5QPTcV4Y1bAQb5R?si=FIG982vkS-2P4Oj6VDzWng).

### User Overrides
The user will be able to override the color for genres (each album is given a set of tags, we can make a database of the genres a user has listened to). User will also be able to modify the default color gradient, tweak settings for the song analysis, and merge genre tags (i.e. merge 'metalcore' and 'thrash-metal', and make songs with those tags use the same colors.)

