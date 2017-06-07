import httplib2
import json
import sys

def getGeocodeLocation(inputString):
	key="AIzaSyC2llFhfEmr9uz0Wl4CxreAWE7-GedqUvQ"
	location=inputString.replace(" ","+")
	url=('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' %(location, key))
	h=httplib2.Http()
	response, content =h.request(url, 'GET')
	result = json.loads(content)
	#print result['results'][0]['geometry']['location']['lat']
	#print result['results'][0]['geometry']['location']['lng']
	return str(result['results'][0]['geometry']['location']['lat']), str(result['results'][0]['geometry']['location']['lng'])

#if __name__=="__main__":
	#getGeocodeLocation(sys.argv[1])