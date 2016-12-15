import json, urllib, urllib2, datetime
from time import gmtime, strftime


key_gen = open("keys.txt", "r").read().strip().split("\n")[0]
key_emb = open("keys.txt", "r").read().strip().split("\n")[1]

# ================================================
#               Google API Helpers
# ================================================
def webstring(adr):
    return "+".join(adr.split())

# ================================================
#                   Geolocation
# ================================================
def call_gl():
    gl_url = "https://www.googleapis.com/geolocation/v1/geolocate?key=%s"%(key_gen)
    d = urllib.urlencode( {} )
    gl_data = urllib2.urlopen(url=gl_url, data=d)
    gl_get = gl_data.read()
    gl_dict = json.loads(gl_get)
    return gl_dict

def gl_location():
    gl_dict = call_gl()
    return [gl_dict['location']['lat'],
            gl_dict['location']['lng']]

# print gl_location()

# ================================================
#                   Geocoding
# ================================================
def call_gc_ll(lat, lng): 
    gc_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s"%(lat,lng,key_gen)
    gc_data = urllib2.urlopen(gc_url)
    gc_get = gc_data.read()
    gc_dict = json.loads(gc_get)
    return gc_dict

def call_gc_ad(adr):
    add = webstring(adr)
    gc_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s,NY&components=country:US&key=%s"%(add,key_gen)
    gc_data = urllib2.urlopen(gc_url)
    gc_get = gc_data.read()
    gc_dict = json.loads(gc_get)
    return gc_dict
    
def gc_address(lat, lng):
    gc_dict = call_gc_ll(lat, lng)
    return gc_dict['results'][0]['formatted_address']

def gc_latlng(adr):
    gc_dict = call_gc_ad(adr)
    return [gc_dict['results'][0]['geometry']['location']['lat'],
            gc_dict['results'][0]['geometry']['location']['lng']]

# print gc_latlng("345 Chambers Street, NY 10282")

# ================================================
#                Distance Matrix
# ================================================
def call_dm(lat1, lng1, lat2, lng2, mode=None):
    add1_raw = gc_address(lat1,lng1)
    add1 = webstring(add1_raw)
    add2_raw = gc_address(lat2,lng2)
    add2 = webstring(add2_raw)
    print lat1, lng1, lat2, lng2
    tmode = ""
    if mode is not None:
        tmode = mode
    dm_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%s&destinations=%s&mode=%s&key=%s"%(add1,add2,tmode,key_gen)
    dm_data = urllib2.urlopen(dm_url)
    dm_get = dm_data.read()
    dm_dict = json.loads(dm_get)
    return dm_dict

def dm_eta(lat1, lng1, lat2, lng2, mode=None):
    if mode is None:
        dm_dict = call_dm(lat1, lng1, lat2, lng2) # Perhaps Remove In Future
    else:
        dm_dict = call_dm(lat1, lng1, lat2, lng2, mode)
    return int(dm_dict['rows'][0]['elements'][0]['duration']['value']) / 60

def dm_dist(lat1, lng1, lat2, lng2, mode=None):
    dm_dict = call_dm(lat1, lng1, lat2, lng2)
    return dm_dict['rows'][0]['elements'][0]['distance']['value']

# d1 = gl_location()
# d2 = ["40.7925920","-73.8465270"]
# print "Estimated Time: ", dm_eta(d1[0],d1[1],d2[0],d2[1],"walking")
# print "Distance: ", dm_dist(d1[0],d1[1],d2[0],d2[1])

# ================================================
#                Directions API
# ================================================

def get_directions_dict(origin, destination, mode):
    new_origin = webstring(origin)
    new_destination = webstring(destination)
    if mode == "":
        dm_url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s"%(new_origin, new_destination, key_gen)
    else:
        dm_url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&mode=%s&key=%s"%(new_origin, new_destination, mode, key_gen)
    dm_data = urllib2.urlopen(dm_url)
    dm_get = dm_data.read()
    dm_dict = json.loads(dm_get)
    print dm_url
    return dm_dict

def get_map_link(origin, destination, mode):
    new_origin = webstring(origin)
    new_destination = webstring(destination)
    base_url = "https://maps.google.com/maps/embed/v1/directions?mode=%s&origin=%s&destination=%s&key=%s"%(mode, new_origin, new_destination, key_emb)
    return base_url

def get_trip_duration(dm_dict):
    arrival_time = dm_dict["routes"][0]["legs"][0]["arrival_time"]["text"]
    departure_time = dm_dict["routes"][0]["legs"][0]["departure_time"]["text"]
    indexOfArrival = arrival_time.find(":")
    indexOfDeparture = departure_time.find(":")
    hour_arrival = int(arrival_time[0:indexOfArrival])
    hour_departure = int(departure_time[0:indexOfDeparture])
    if hour_arrival == 12 and arrival_time[-2] == 'a':
        hour_arrival = 0
    elif arrival_time[-2]== 'p' and arrival_time[0:2] != 12:
        hour_arrival += 12
    if hour_departure == 12 and departure_time[-2] == 'a':
        hour_departure = 0
    elif departure_time[-2] == 'p':
        hour_departure += 12
    arrival_minutes = (hour_arrival * 60) + int(arrival_time[indexOfArrival + 1: indexOfArrival + 3])
    departure_minutes = (hour_departure * 60) + int(departure_time[indexOfDeparture + 1: indexOfDeparture + 3])
    if (arrival_minutes - departure_minutes) >= 0:
        return arrival_minutes - departure_minutes
    elif (arrival_minutes - departure_minutes) < 0:
        return (arrival_minutes + 1440) - departure_minutes

def get_ETA(dm_dict):
    arrival_time = dm_dict["routes"][0]["legs"][0]["arrival_time"]["text"]
    return arrival_time

def get_distance(dm_dict):
    distance = dm_dict["routes"][0]["legs"][0]["distance"]["text"]
    return distance

def get_directions_driving(origin, destination):
    dm_dict = get_directions_dict(origin, destination, "driving")
    steps = dm_dict["routes"][0]["legs"][0]["steps"]
#    line_counter = 0
    retStr = ""
    for item in steps:
        retStr += item["html_instructions"] + "<br>"
#        line_counter += 1
#    print line_counter
    return retStr

def get_directions_transit(origin, destination):
    dm_dict = get_directions_dict(origin, destination, "transit")
    data = dm_dict['routes'][0]['legs'][0]['steps']
    step = 0;
    retStr = ""
    for i in data:
        step += 1;
        retStr += "Step " + str(step) + ":<br>"
        retStr += i['html_instructions'] + "<br>"
        mode = i['travel_mode']
        if (mode == "WALKING"):
            for direction in i['steps']:
                if 'html_instructions' in direction:
                    retStr += direction['html_instructions'] + "<br>"
        elif (mode == "TRANSIT"):
            details = i['transit_details']
            retStr += details['departure_stop']['name'] + " to " + details['arrival_stop']['name'] + "<br>"
            retStr += "Take the "
            if 'short_name' in details['line']:
                retStr += details['line']['short_name'] + " train "
            elif 'name' in details['line']:
                retStr += details['line']['name'] + " "
            retStr += str(details['num_stops']) + " stops towards " + details['headsign'] + "<br>"
        retStr += "\n"
    return retStr

def get_directions_walking(origin, destination):
    dm_dict = get_directions_dict(origin, destination, "walking")
    steps = dm_dict["routes"][0]["legs"][0]["steps"]
    line_counter = 0
    retStr = ""
    for item in steps:
        retStr += item["html_instructions"] + "<br>"
        line_counter += 1
    print line_counter
    return retStr

def get_directions_bicycling(origin, destination):
    dm_dict = get_directions_dict(origin, destination, "bicycling")
    steps = dm_dict["routes"][0]["legs"][0]["steps"]
    line_counter = 0
    retStr = ""
    for item in steps:
        retStr += item["html_instructions"] + "<br>"
        line_counter += 1
    print line_counter
    return retStr

def time_difference(eta, arrival_time):
    current_time = strftime("%H:%M")
    trip_duration = eta
    indexOfArrival = arrival_time.find(":")
    indexOfDeparture = current_time.find(":")
    hour_arrival = int(arrival_time[0:indexOfArrival])
    hour_departure = int(current_time[0:indexOfDeparture])
    print("arrival" + str(hour_arrival))
    print("departure" + str(hour_departure))
    # if hour_arrival == 12 and arrival_time[-2] == 'a':
    #     hour_arrival = 0
    # elif arrival_time[-2]== 'p' and arrival_time[0:2] != 12:
    #     hour_arrival += 12
    # if hour_departure == 12 and departure_time[-2] == 'a':
    #     hour_departure = 0
    # elif departure_time[-2] == 'p':
    #     hour_departure += 12
    arrival_minutes = (hour_arrival * 60) + int(arrival_time[indexOfArrival + 1: indexOfArrival + 3])
    departure_minutes = (hour_departure * 60) + int(current_time[indexOfDeparture + 1: indexOfDeparture + 3])
    difference = abs(departure_minutes - arrival_minutes)
    return trip_duration - difference


# UNNECESSARY
#def get_detailed_directions(dm_dict):
#    steps = dm_dict["routes"][0]["legs"][0]["steps"][0]["steps"]
#    line_counter = 0
#    retStr = ""
#    for item in steps:
#        retStr += item["html_instructions"] + "\n"
#        line_counter += 1
#    print line_counter
#    return retStr

# print get_directions_transit("345 Chambers Street", "67-41 Burns Street")
#dm_dict = get_directions_dict("Little Neck", "Penn Station", "driving")
#print get_directions_bicycling("Times Square", "Penn Station")