#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, urllib2, datetime

# API Key: 8312fc029e352953b9e6ed8ca0202eb9Y

# ================================================
#                DarkSky API Calls
# ================================================
# Notes: Currently, functions only work on the
#		next 48 hours, using offsets in minutes
#		(max minute offset seems to be 2910)
# ================================================

masterURL = "https://api.darksky.net/forecast/8312fc029e352953b9e6ed8ca0202eb9/"

#------------------------------------------------------------------------------------------------------------------------------------------------------
#############
##FUNCTIONS##
#############
#------------------------------------------------------------------------------------------------------------------------------------------------------

def genURL(x, y):
	return "https://api.darksky.net/forecast/8312fc029e352953b9e6ed8ca0202eb9/" + str(x) + "," + str(y)

def convertTime(time, flag):
	if (flag == 1):
		return datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S')
	if (flag == 2):
		return datetime.datetime.fromtimestamp(time).strftime('%m-%d-%Y')
	else:
		return datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S -- %m-%d-%Y')

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
		return rainchance * 100
	if (offset > 60):
		hourly = reqdict["hourly"]
		closestHour = closestHourOffset(offset)
		hourlydata = hourly["data"][closestHour]
		precip = hourlydata["precipProbability"]
		return rainchance * 100
	else:
		rainchance = currently["precipProbability"]
		return rainchance * 100

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

def getSunset(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	daily = reqdict["daily"]
	dailydata = daily["data"][offset]
	return dailydata["sunsetTime"]

def getSunrise(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	daily = reqdict["daily"]
	dailydata = daily["data"][offset]
	return dailydata["sunriseTime"]

def getPrecipType(x, y, offset):
	if (getIntensity(x, y, offset) == 0):
		return "none"
	else:
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
			precip = raindata["precipType"]
			return precip
		if (offset > 60):
			hourly = reqdict["hourly"]
			closestHour = closestHourOffset(offset)
			hourlydata = hourly["data"][closestHour]
			precip = hourlydata["precipType"]
			return precip
		else:
			precip = currently["precipType"]
			return precip

def getIcon(x, y, offset):
	url = genURL(x, y)
	curr = urllib2.urlopen(url)
	req = curr.read()
	reqdict = json.loads(req)
	currently = reqdict["currently"]
	minutely = reqdict["minutely"]
	minutelydata = minutely["data"]
	if (offset == 0):
		icon = currently["icon"]
		return icon
	else:
		hourly = reqdict["hourly"]
		closestHour = closestHourOffset(offset)
		hourlydata = hourly["data"][closestHour]
		icon = hourlydata["icon"]
		return icon







	






