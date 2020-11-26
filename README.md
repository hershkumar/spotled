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


Server will be run on an RPI, probably gonna interface with the LEDs via gpio (Or ideally we have some wireless way of connecting to the lights from the rpi). GPIO isn't my ideal solution because thats kinda icky, but it might be the only option, seeing as that's what everyone on the internet seems to use.

Useful links:
https://dordnung.de/raspberrypi-ledstrip/

Seems to be basically 3 mosfets and a power adapter.