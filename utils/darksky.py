#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, urllib2, datetime

# API Key: 8312fc029e352953b9e6ed8ca0202eb9Y

# ================================================
#                DarkSky API Calls
# ================================================

masterURL = "https://api.darksky.net/forecast/8312fc029e352953b9e6ed8ca0202eb9/"

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

#------------------------------------------------------------------------------------------------------------------------------------------------------
###############
##GLOBAL DATA##
###############
#------------------------------------------------------------------------------------------------------------------------------------------------------

def genURL(x, y):
	return "https://api.darksky.net/forecast/8312fc029e352953b9e6ed8ca0202eb9/" + str(x) + "," + str(y)

def closestHourOffset(minoffset):
	hours = 0
	minutes = 0
	while (minoffset > 60):
		minoffset = minoffset - 60
		hours += 1
	minutes = minoffset
	if (minutes > 30):
		hours += 1
		minutes = 0
	else:
		minutes = 0
	return hours

def getRainChance(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	minutely = reqdict["minutely"]
	minutelydata = minutely["data"]
	if (offset > 0 and offset < 61):
		raindata = minutelydata[offset]
		time = raindata["time"]
		rainchance = raindata["precipProbability"]
		return rainchance
	else:
		rainchance = currently["precipProbability"]
		return rainchance

def getWind(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	hourly = reqdict["hourly"]
	closestHour = closestHourOffset(offset)
	hourlydata = hourly["data"][closestHour]
	if (offset == 0):
		hourlydata = currently
	wind = hourlydata["windSpeed"]
	return wind

def getStatus(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	hourly = reqdict["hourly"]
	closestHour = closestHourOffset(offset)
	hourlydata = hourly["data"][closestHour]
	if (offset == 0):
		hourlydata = currently
	status = hourlydata["summary"]
	return status

def getTemp(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	hourly = reqdict["hourly"]
	closestHour = closestHourOffset(offset)
	hourlydata = hourly["data"][closestHour]
	if (offset == 0):
		hourlydata = currently
	temp = hourlydata["temperature"]
	return temp

def getFeel(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	hourly = reqdict["hourly"]
	url = genURL(x, y)
	closestHour = closestHourOffset(offset)
	hourlydata = hourly["data"][closestHour]
	if (offset == 0):
		hourlydata = currently
	feel = hourlydata["apparentTemperature"]
	return feel

def getIntensity(x, y, offset):
	url = genURL(x, y)
	print(url)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	hourly = reqdict["hourly"]
	closestHour = closestHourOffset(offset)
	hourlydata = hourly["data"][closestHour]
	if (offset == 0):
		hourlydata = currently
	intensity = hourlydata["precipIntensity"]
	return intensity


print(getRainChance(40.7925920, -73.9465270, 485))








	






