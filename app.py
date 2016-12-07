from flask import Flask, url_for, redirect, render_template, session, request
from utils import mta, google, darksky

app = Flask(__name__)
app.secret_key = "Welcome to the DNC!!!!!!!!"

#############-------------------------------------------------------------------------------------------------------------------------------------------
##FUNCTIONS##
#############-------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/", methods=["POST","GET"])
def root():
    return render_template("main.html",
                           title="DoesNotCommute")

@app.route("/result", methods=["POST","GET"])
def results():
    if request.method == 'POST':
        # Current Coordinates 
	currentCoordinates = google.gl_location() #array [x, y]
	if ('location' in request.form):
            currentCoordinates = request.form['location']
            currentCoordinates = google.gc_latlng(currentCoordinates)

        # Destination Coordinates
	destination = request.form['destination']
	destinationCoordinates = google.gc_latlng(destination)

        # Transport Mode
	transport = request.form['transportMode']
        
        # ============= DATA RETRIEVAL ==============
        # ETA
        eta = google.dm_eta(currentCoordinates[0], currentCoordinates[1],
                            destinationCoordinates[0], destinationCoordinates[1])
        eta = int(eta) / 60

        # Weather
        currentWeather = darksky.getStatus(currentCoordinates[0], currentCoordinates[1], eta)
        destinationWeather = darksky.getStatus(destinationCoordinates[0], destinationCoordinates[1], eta)

    return str(currentCoordinates) + "<br>" + str(destinationCoordinates) + "<br>" + str(transport) + "<br>" + str(eta) + "<br>" + str(currentWeather) + "<br>" + str(destinationWeather)
    # print(currentCoordinates)
    # print(destinationCoordinates)
    # return render_template("results.html",
    # title="Trip Results")


@app.route("/about/", methods=["POST","GET"])
def about():
    return render_template("main.html",
                           title="About")

@app.route("/test/", methods=["GET"])
def test():
#    return render_template("testMap.html", embed= "https://maps.google.com/maps/embed/v1/directions?mode=transit&origin=%22Stuyvesant+High+School&destination=42-25+247th+St,+Flushing,+NY+11363&key=AIzaSyD96prG2oU4bKyCxWN3fge3TVJKGKm3Zrw")
    return render_template("testMap.html",
                       embed= google.get_map_link("Little Neck", "Stuyvesant High School", "transit"))

# Running The App
if __name__ == "__main__":
    app.debug = True
    app.run()


        
