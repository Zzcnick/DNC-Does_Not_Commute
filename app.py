from flask import Flask,url_for,redirect,render_template,session, request
from utils import mta, google, darksky

app = Flask(__name__)
app.secret_key = "Welcome to the DNC"

@app.route("/", methods=["POST","GET"])
def root():
    return render_template("main.html",
                           title="Welcome")

@app.route("/about/", methods=["POST","GET"])
def about():
    return render_template("main.html",
                           title="About")

# Running The App
if __name__ == "__main__":
    app.debug = True
    app.run()


        
