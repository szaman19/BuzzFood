import requests
import foursquare
import json
import os

def getImageUrls(query):
	key = "AIzaSyBNWmypZhvryr_CUmVfJ8h1NLqWdfyIJDA"
	cx = "018347742159790243558:yjmlvg2ulxg"
	searchType = "image"

	params = {
		"key": key,
		"cx" : cx,
		"q":query,
		"searchType":searchType,
	}
	url = "https://www.googleapis.com/customsearch/v1"

	r = requests.get(url,params=params)
	jsonDump = json.dumps(r.json())
	searchResults = json.loads(jsonDump)

	imageUrlDict = {}
	for result in searchResults["items"]:
		## Key is url of thumbnail, value is link to full image
		imageUrlDict[result['image']['thumbnailLink'].encode('utf-8')] = result['link'].encode('utf-8')

	return imageUrlDict

def getTags(imageUrlDict):
	imageUrlValues = imageUrlDict.values()
	tagDict = {}

	for imageURL in imageUrlValues:
		header = {'Authorization' : "Bearer 9PLrJMMB6sl4qoSK8JPf8gy9mRVfvL"}
		data = {'model' : "food-items-v0.1", 'url' : imageURL}

		r = requests.get("https://api.clarifai.com/v1/tag/",headers = header,params=data)
		JSONTags = r.json()

		tagData = JSONTags['results'][0]['result']['tag']
		tagList = zip(tagData['classes'],tagData['probs'])

		for tag in tagList:
			if tag[1] > .8:
				tagName = tag[0].encode()
				if not tagDict.has_key(tagName):
					tagDict[tagName] = 0
				tagDict[tagName] += 1

	return tagDict

def fourSearch(tagDict):
	clientID = 'JD5WEQCZLAOXXPVBYZV1TOUONBMWCUXNHCJALUSQN5YTUHKA'
	clientSecret = '1QW0UZYHRAVPJGCWA04JSJGHJ0RWEPW3XG3AF3GYJFUTYQRU'
	client = foursquare.Foursquare(client_id = clientID, client_secret = clientSecret)

	restaurantDict = {}
	tagKeys = tagDict.keys()
	location = '40.7289792,-73.9956687'

	for tag in tagKeys:
		restaurants = client.venues.search(params={'ll' : location, 'query': tag, 'limit' : '10', 'categoryId' : '4d4b7105d754a06374d81259'})['venues']
		for restaurant in restaurants:
			restaurantID = restaurant['id'].encode('utf-8')
			if not restaurantDict.has_key(restaurantID):
				restaurantDict[restaurantID] = 0.0
			restaurantDict[restaurantID] += tagDict[tag] / float(len(tagKeys))

	return restaurantDict

def restaurantRank(restaurantDict):
	matchValue = sorted(set(restaurantDict.values()))
	return matchValue

def main():
##	imageUrlDict = getImageUrls("food")
	imageUrlDict = {'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSq4RxycF0BLa1xbBh3MhKhl7uqN-YdbGu8uHoCACyn3yUn3qKJr0C-2RYz': 'http://media4.popsugar-assets.com/files/2013/07/02/953/n/1922195/426ebedb72d4cbbd_taste-the-states-cover.xxxlarge/i/US-State-Foods.jpg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9_x4IhsaCSKSsnjrtfX920IpOsU2fGktKUGICSf0Bio13WvCAITy2NOgx': 'http://www.healthyfoodteam.com/wp-content/uploads/2014/02/Which-Food-You-Should-Never-Mix.jpg', 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTAKAkjZvDkDTJc3Q9iqfGU6x7ywv6oeD8hlpvzE0I6glrXvcU7-eDcebpu': 'http://travelchannel.sndimg.com/content/dam/images/travel/fullset/2014/08/20/63/food-paradise-106-burritos-ss-003', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWJWbrqRHY4_KJVdYVxd4PvHzRqFjZInhDy1NDRcslhCM3QLObWIBb4fz7': 'http://travelchannel.sndimg.com/content/dam/images/travel/fullset/2015/03/24/bizarre-foods-delicious-destinations-112-hong-kong-ss/bizarre-foods-delicious-destinations-ss-038-hong-kong-typhoon-shelter-crab.jpg.rend.tccom.1280.960.jpeg', 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRiceNRzk1Y9uwJLg2s3gAGj_5s5HVhlmaYSXb7lOEvQv3SIdlBGeHYQGje': 'https://i.ytimg.com/vi/uDnd_C8Hkp8/maxresdefault.jpg', 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSAnOj2m37X-mEqppiSQz1osMIVj1O5Ar9oBNIR64T0bwWjhHM3aAjMipHi': 'http://d.fastcompany.net/multisite_files/fastcompany/imagecache/1280/poster/2015/01/3041647-poster-p-1-most-innovative-companies-2015-next-sectors-food.jpg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHhW_JNH2I6A1XmeDv29KhyiYCjlIbZZqUvmMVoDsDcvT1E05FgXLcqBs': 'https://i.ytimg.com/vi/SeTpJNRnG6w/maxresdefault.jpg', 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTcrqYznCNDlIoi3r6VzpYM_F9E-iYkbMPYdr3NtCQ0nfAdV5g-Khs3hlM': 'http://cdn.playbuzz.com/cdn/39f85817-18ad-4321-9908-03b342872b87/7838a2f8-fb2d-48e8-abc9-f7db942d3ede.jpg', 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT_bTJKkp6AzOw1DYp_ab0LqgczobdHuH3jZky_slSiUtYzFf2qmlpetmg': 'https://pixabay.com/static/uploads/photo/2015/07/30/18/23/burger-868145_960_720.jpg', 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSJkwTZV-vDHcrJkwKFdcc20iqbUjKh-NwW3lMJN5Jmko3YUJ0j7mhOAfq4': 'https://i.ytimg.com/vi/JWsob3MZUQ4/maxresdefault.jpg'}
	tags = getTags(imageUrlDict)
	print tags
	search = fourSearch(tags)
	print json.dumps(search, indent=4, sort_keys=True)
	print restaurantRank(search)

main()