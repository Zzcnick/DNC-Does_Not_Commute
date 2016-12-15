# Does Not Commute

DoesNotCommute is an all in one commuter app made by New Yorkers, for New Yorkers.

Using information from Google Maps and DarkSky, we provide users with reliable, up-to-date information and statistics regarding their commute. We provide it all: from optimal routes, to delays, to alerts, to weather.

Whatever might get in your way from point A to point B, we'll give you the latest. We've got you covered; you'll never be late again with the help of our fast and efficient app!

### Installation Instructions

In order to run this on your client, you will need Flask and Python. 
Download the files to a directory, and run the app using `python app.py`. 

### Usage Instructions

Once the app is running, navigate to `127.0.0.1:5000/` on a web browser and the website will load.
To use the app, enter a starting location (if none is provided, it will automatically choose a location near your current location) and a destination. Afterwards, choose a mode of transportation. Finally, enter a desired time of arrival and submit the form. If the app cannot find the location, it will ask the user to enter new information.

The app will then redirect the user to a website that includes a map, the weather, and directions on how to get to the destination. There are separate tabs that the user may click through to view all of the provided information.
