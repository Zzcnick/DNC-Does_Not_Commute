from flask import Flask,url_for,redirect,render_template,session, request
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
		currentCoordinates = google.gl_location() #array [x, y]
		transport = request.form['transportMode']
		if ('location' in request.form):
			currentCoordinates = request.form['location']
			currentCoordinates = google.gc_latlng(currentCoordinates)
		destination = request.form['destination']
		destinationCoordinates = google.gc_latlng(destination)
	print(currentCoordinates)
	print(destinationCoordinates)




	return render_template("results.html",
							title="Trip Results")


@app.route("/about/", methods=["POST","GET"])
def about():
    return render_template("main.html",
                           title="About")

# Running The App
if __name__ == "__main__":
    app.debug = True
    app.run()


        
