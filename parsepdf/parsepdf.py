# CONVERT FROM PDF TO XML
from subprocess import call
from geopy import geocoders

import xml.dom.minidom
from xml.dom.minidom import Node

# FIXME: XML OUTPUT FAILS, DOESN'T DISPLAY WRITE ANY ESTABLISHMENT INFO, PROBLEM WITH USING TWO LISTS

#subprocess.Popen('echo "pdftohtml -i -xml -noframes -nomerge -nodrm data.pdf"', shell=True)

# CREATE OBJECT FOR EACH DATA AND STORE IN A LIST/ARRAY
# from data.xml
class Establishment :
    pass

# LOAD DATA.XML
doc = xml.dom.minidom.parse("shorttestdata.xml")

# PARSE DATA.XML
estlist = []

currentNodeAttributeTop = 0
previousNodeAttributeTop = 0

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# TODO: Create establishment reset and create method

est = Establishment()
est.name = ''
est.address = ''
est.postcode = ''
est.inspectiondate = ''
est.score = ''
est.classification = ''
# from geocoding
est.lat = ''
est.lng = ''
#est.accuracy = ''

# TODO: Create method to filter nodes rather than repeating it below

for node in doc.getElementsByTagName("text") :   
    currentNodeAttributeTop = node.getAttribute("top")
    if currentNodeAttributeTop == previousNodeAttributeTop :
        # same row
        if node.getAttribute("left") == "84" :
            est.name = getText(node.childNodes) # FIXME: name is not being output
        elif node.getAttribute("left") == "466" :
            est.address = getText(node.childNodes)
        elif node.getAttribute("left") == "717" :
            est.postcode = getText(node.childNodes)
        elif (node.getAttribute("left") == "817"
           or node.getAttribute("left") == "818"
           or node.getAttribute("left") == "819"
           or node.getAttribute("left") == "820"
           or node.getAttribute("left") == "821"
           or node.getAttribute("left") == "822"
           or node.getAttribute("left") == "823") :
            est.inspectiondate = getText(node.childNodes)
        elif (node.getAttribute("left") == "946"
           or node.getAttribute("left") == "950"    # Score is 0 or 5
           or node.getAttribute("left") == "943") : # Score is 100
            est.score = getText(node.childNodes)
        elif node.getAttribute("left") == "989" :
            est.classification = getText(node.childNodes)
        else :
            print "ELEMENT UNKNOWN: %s" %(node.toxml())
        #print "---> SAME ROW"
    else :
        # new row
        estlist.append(est)
        est = Establishment()
        est.name = ''
        est.address = ''
        est.postcode = ''
        est.inspectiondate = ''
        est.score = ''
        est.classification = ''
        #should come from geocoding later
        est.lat = ''
        est.lng = ''
        #est.accuracy = ''
        #print "---> NEW ROW"
        if node.getAttribute("left") == "84" :
            est.name = getText(node.childNodes) # FIXME: name is not being output
        elif node.getAttribute("left") == "466" :
            est.address = getText(node.childNodes)
        elif node.getAttribute("left") == "717" :
            est.postcode = getText(node.childNodes)
        elif (node.getAttribute("left") == "817"
           or node.getAttribute("left") == "818"
           or node.getAttribute("left") == "819"
           or node.getAttribute("left") == "820"
           or node.getAttribute("left") == "821"
           or node.getAttribute("left") == "822"
           or node.getAttribute("left") == "823") :
            est.inspectiondate = getText(node.childNodes)
        elif (node.getAttribute("left") == "946"
           or node.getAttribute("left") == "950"    # Score is 0 or 5
           or node.getAttribute("left") == "943") : # Score is 100
            est.score = getText(node.childNodes)
        elif node.getAttribute("left") == "989" :
            est.classification = getText(node.childNodes)
        else :
            print "ELEMENT UNKNOWN: %s" %(node.toxml())
    previousNodeAttributeTop = currentNodeAttributeTop
    currentNodeAttributeTop = node.getAttribute("top")
estlist.append(est) # TODO: What if the last node is empty?

print "XML read complete."
print 'Establishments: %s' % len(estlist)

# DATA CLEANING AND GEOCODING
#http://philsturgeon.co.uk/blog/2011/02/geocoding-apis-compared
#http://code.google.com/p/geopy/wiki/GettingStarted

geoestlist = [] # list of all establishments with coordinates

class LocationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

for est in estlist :
    # TODO: DATA CLEANING
        # find blank elements
        # remove first element (containing table headings)
        # trailing or leading spaces
        # Check that all locations are rougly in the Hull area
            # if ( lat > 52.5 and lat < 53.9 and lng < -0.4 and lng > -0.25) :
        
    # GEOCODING
    try :
        g = geocoders.Google(domain='maps.google.co.uk')
        place, (lat, lng) = g.geocode('%s, %s' %(est.address, est.postcode))
        #print "%s: %.5f, %.5f" % (place, lat, lng)
        est.lat = str(lat)
        est.lng = str(lng)
        #est.accuracy = accuracy
        #estlist.pop(est)
        geoestlist.append(est)

    except :
        print('GEOCODING FAILURE: %s, %s, %s' %(est.name, est.address, est.postcode))
        # TODO: Try other geocoding services, and/or use just postcode on failure

print 'Establishments: %s' % len(estlist)
print 'Geocoded establishments: %s' % len(geoestlist)

# PRINT XML (FIT FOR A KING, ...OR GOOGLE MAPS API)
#<markers>
#<marker name="" address="" postcode="" lat="" lng="" accuracy="" score="" classification=""/>
#</markers>

outdoc = xml.dom.minidom.Document()

# Create the <markers> base element
markers = outdoc.createElement("markers")
outdoc.appendChild(markers)

for est in geoestlist :
    # Create <marker> element
    marker = doc.createElement("marker")
    marker.setAttribute("name", est.name)
    marker.setAttribute("address", est.address)
    marker.setAttribute("postcode", est.postcode)
    marker.setAttribute("lat", est.lat)
    marker.setAttribute("lng", est.lng)
    #marker.setAttribute("accuracy", est.accuracy)
    marker.setAttribute("score", est.score)
    marker.setAttribute("classification", est.classification)
    markers.appendChild(marker)

# Print our newly created XML
#print outdoc.toprettyxml(indent="  ")

f = open("data_output.xml", "w")
try:
    f.write(outdoc.toprettyxml(indent="  "))
finally:
    f.close()
 
print "End"

