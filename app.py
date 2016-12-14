from flask import Flask, url_for, redirect, render_template, session, request
from utils import google, darksky

app = Flask(__name__)
app.secret_key = "Welcome to the DNC!!!!!!!!"

#############
##FUNCTIONS##
#############

@app.route("/", methods=["POST","GET"])
def root():
	return render_template("main.html",
							title="DoesNOTCommute")

@app.route("/result", methods=["POST","GET"])
def results():
        # ============= DATA RETRIEVAL ==============
        if request.method == 'GET':
		return redirect(url_for("root"))
        currentCoordinates = google.gl_location() #array [x, y]
	if ('location' in request.form and request.form['location'] != 'current_location'):
		currentCoordinates = request.form['location']
		currentCoordinates = google.gc_latlng(currentCoordinates)

	# Destination Coordinates
	destination = request.form['destination']
	destinationCoordinates = google.gc_latlng(destination)

	# Transport Mode
	transport = str(request.form['transportMode'])
	
	# ETA
	eta = google.dm_eta(currentCoordinates[0], currentCoordinates[1],
		            destinationCoordinates[0], destinationCoordinates[1],
                            transport)

	# Weather
	currentWeather = darksky.getWeatherDict(currentCoordinates[0], currentCoordinates[1], 0)
	destinationWeather = darksky.getWeatherDict(destinationCoordinates[0], destinationCoordinates[1], eta)

	currentAddress = google.gc_address(currentCoordinates[0], currentCoordinates[1])
	destinationAddress = google.gc_address(destinationCoordinates[0], destinationCoordinates[1])

        # Directions
        if transport == 'walking':
                directionDetails = google.get_directions_walking(currentAddress, destinationAddress)
        elif transport == 'driving':
                directionDetails = google.get_directions_driving(currentAddress, destinationAddress)
        elif transport == 'transit':
                directionDetails = google.get_directions_transit(currentAddress, destinationAddress)
        elif transport == 'bicycling':
                directionDetails = google.get_directions_bicycling(currentAddress, destinationAddress)

        # ============= TEMPLATING ==============
	return render_template("results.html",
                               title="Trip Results",
                               cstatus = currentWeather["status"],
                               ctemp = currentWeather["temp"],
                               cprecipType = currentWeather["precipType"],
                               cfeel = currentWeather["feel"],
                               crainChance = currentWeather["rainChance"],
                               cintensity = currentWeather["intensity"],
                               csunset = darksky.convertTime(currentWeather["sunset"], 1),
                               csunrise = darksky.convertTime(currentWeather["sunrise"], 1),
                               cwind = currentWeather["wind"],
                               cicon = currentWeather["icon"],
                               dstatus = destinationWeather["status"],
                               dtemp = destinationWeather["temp"],
                               dprecipType = destinationWeather["precipType"],
                               dfeel = destinationWeather["feel"],
                               drainChance = destinationWeather["rainChance"],
                               dintensity = destinationWeather["intensity"],
                               dsunset = darksky.convertTime(destinationWeather["sunset"], 1),
                               dsunrise = darksky.convertTime(destinationWeather["sunrise"], 1),
                               dwind = destinationWeather["wind"],
                               dicon = destinationWeather["icon"],
                               caddress = currentAddress,
                               daddress = destinationAddress,
                               maplink = google.get_map_link(currentAddress, destinationAddress, transport),
                               directions = directionDetails,
                               etime = eta
        )


@app.route("/about/", methods=["POST","GET"])
def about():
	return render_template("about.html",
							title="About DNC")

@app.route("/test/", methods=["GET"])
def test():
	return render_template("testMap.html",
							embed= google.get_map_link("Little Neck", "Stuyvesant High School", "transit"))

# Running The App
if __name__ == "__main__":
	app.debug = True
	app.run()



