import DBConnection
from math import sin, cos, sqrt, atan2, radians
import time

class Location:
    def __init__(self, parcelid, longitude, latitude, distance):
        self.parcelid = parcelid
        self.longitude = longitude
        self.latitude = latitude
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance

def getDistance(point1, point2):
    R = 6373.0
    lon1 = radians(point1[0])
    lat1 = radians(point1[1])
    lon2 = radians(point2[0])
    lat2 = radians(point2[1])

    dlon = lon1 - lon2
    dlat = lat1 - lat2
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

def getLocations(origin, number, list):
    millis1 = int(round(time.time() * 1000))
    rows = DBConnection.execute_query("""SELECT * FROM locations""")
    for row in rows:
        longitude =float( int(row[2]))/1000000
        latitude = float(int(row[1]))/1000000
        point = [longitude, latitude]
        distance = getDistance(origin, point)
        if len(list) < number:
            newlocation = Location(row[0], longitude, latitude, distance)
            list.append(newlocation)
            list.sort()
        elif distance < list[number - 1].distance:
            del list[number - 1]
            newlocation = Location(row[0], longitude, latitude, distance)
            list.append(newlocation)
            list.sort()
        else:
            continue
    millis2 = int(round(time.time() * 1000))
    time1 = float(millis2 - millis1) / 1000
    generateResponse(list, time1)

def generateResponse(list, time):
    with open('/home/ubuntu/flaskapp/locations.html','w') as myFile:
        myFile.write('<html>')
        myFile.write('<body>')
        myFile.write('<head>')
        myFile.write('rows in set: ' + str(time) + ' sec')
        myFile.write('</head></br>')
        myFile.write('</br>')
        myFile.write('<table border="3">')
        myFile.write('<tr>'
                     + '<th>Parcelid</th>'
                     + '<th>Longitude</th>'
                     + '<th>Latitude</th>'
                     + '<th>Distance</th>'
                     +'</tr>')
        for location in list:
            myFile.write('<tr>'
                         + '<th>'+ str(location.parcelid) +'</th>'
                         + '<td>'+ str(location.longitude) +'</td>'
                         + '<td>'+ str(location.latitude) +'</td>'
                         + '<td>'+ str(location.distance) +'</td>'
                         + '</tr>')
        myFile.write('</table>')
        myFile.write('</body>')
        myFile.write('</html>')
