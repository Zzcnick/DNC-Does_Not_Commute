#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, urllib2, datetime

# API Key: 8312fc029e352953b9e6ed8ca0202eb9Y

# ================================================
#                DarkSky API Calls
# ================================================

#Starting Location
clocx = "40.7925920" 
clocy = "-73.9465270"
#Destination Location
plocx = "40.7179460"
plocy = "-74.0139050"


curl = "https://api.darksky.net/forecast/8312fc029e352953b9e6ed8ca0202eb9/" + clocx + "," + clocy
#print curl
ucurr = urllib2.urlopen(curl)
creq = ucurr.read()
creqdict = json.loads(creq)

purl = "https://api.darksky.net/forecast/8312fc029e352953b9e6ed8ca0202eb9/" + plocx + "," + plocy
#print purl
uplan = urllib2.urlopen(purl)
preq = uplan.read()
preqdict = json.loads(preq)

#---------------------------------------------------------------------------------------------------------
#Current Info

ccurrently = creqdict["currently"]
chourly = creqdict["hourly"]
cminutely = creqdict["minutely"]

ctime = datetime.datetime.fromtimestamp(ccurrently["time"]).strftime('%H:%M:%S -- %m-%d-%Y')
ctemp = ccurrently["temperature"]
cstatus = ccurrently["summary"]
cfeel = ccurrently["apparentTemperature"]
cwind = ccurrently["windSpeed"]
crainchance = ccurrently["precipProbability"]

print("The time is currently: " + ctime)
print("Right now, the weather is " + cstatus)
print("The temperature is " + str(ctemp) + "°F")
print("But it feels like " + str(cfeel) + "°F")
print("There is a " + str(cwind) + "mph wind")
print("And there is a " + str(crainchance) + "% chance of rain")

print("\n")
print("Your trip will take 1 hour")
print("\n")
#---------------------------------------------------------------------------------------------------------
#Destination Info

pcurrently = creqdict["currently"]
phourly = preqdict["hourly"]
pminutely = preqdict["minutely"]

phourlydata = phourly["data"] #list of hourly data readings
pminutelydata = pminutely["data"] #list of minutely data readings

raindata = pminutelydata[60]
hourlydata = phourly["data"][1]

ptime = datetime.datetime.fromtimestamp(raindata["time"]).strftime('%H:%M:%S -- %m-%d-%Y')
ptemp = hourlydata["temperature"]
pstatus = hourlydata["summary"]
pfeel = hourlydata["apparentTemperature"]
pwind = hourlydata["windSpeed"]
prainchance = raindata["precipProbability"]

print("When you reach your destination, the time will be " + ptime)
print("The weather will be " + pstatus)
print("The temperature will be " + str(ctemp) + "°F")
print("But it will feel like " + str(pfeel) + "°F")
print("There will be a " + str(pwind) + "mph wind")
print("And there will be a " + str(prainchance) + "% chance of rain")




