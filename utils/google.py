import json, urllib, urllib2

# API Key: AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY

# ================================================
#               Google API Helpers
# ================================================
def webstring(adr):
    return "+".join(adr.split())

# ================================================
#                   Geolocation
# ================================================
def call_gl():
    gl_url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY"
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
    gc_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY"%(lat,lng)
    gc_data = urllib2.urlopen(gc_url)
    gc_get = gc_data.read()
    gc_dict = json.loads(gc_get)
    return gc_dict

def call_gc_ad(adr):
    add = webstring(adr)
    gc_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s,NY&key=AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY"%(add)
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
    dm_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%s&destinations=%s&mode=%s&key=AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY"%(add1,add2,tmode)
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

d1 = gl_location()
d2 = ["40.7925920","-73.8465270"]
print "Estimated Time: ", dm_eta(d1[0],d1[1],d2[0],d2[1],"walking")
# print "Distance: ", dm_dist(d1[0],d1[1],d2[0],d2[1])

# ================================================
#                Directions API
# ================================================

def get_directions(origin, destination, mode = ""):
    new_origin = webstring(origin)
    new_destination = webstring(destination)
    if mode == "":
        dm_url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY"%(new_origin, new_destination)
    else:
        dm_url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&mode=%s&key=AIzaSyCnkOEu9Xyc2O3sNqzmTzCNub6e_kSoUeY"%(new_origin, new_destination, mode)
    dm_data = urllib2.urlopen(dm_url)
    dm_get = dm_data.read()
    dm_dict = json.loads(dm_get)
    return dm_dict

def get_map_link(origin, destination, mode):
    new_origin = webstring(origin)
    new_destination = webstring(destination)
    base_url = "https://maps.google.com/maps/embed/v1/directions?mode=%s&origin=%s&destination=%s&key=AIzaSyD96prG2oU4bKyCxWN3fge3TVJKGKm3Zrw"%(mode, new_origin, new_destination)
    return base_url

def get_trip_duration(dm_dict):
    arrival_time = dm_dict["routes"][0]["legs"][0]["arrival_time"]["text"]
    departure_time = dm_dict["routes"][0]["legs"][0]["departure_time"]["text"]
    return [arrival_time, departure_time]

test_dict = get_directions("Little Neck", "Penn Station", "transit")
print get_trip_duration(test_dict)

#print get_directions("Little Neck", "Penn Station", "transit")["routes"][0]["legs"][0]["arrival_time"]
#print webstring("Stuyvesant High School")
