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

	urlList = []
	for result in searchResults["items"]:
	##	urlList.append(result['image']['thumbnailLink'])
		urlList.append(result['link'].encode('utf-8'))

	print json.dumps(searchResults, indent=4, sort_keys=True)
	print urlList
	return urlList

def getTags(imageURLs):
	tagsDict = {}
	for imageURL in imageURLs:
		header = {'Authorization' : "Bearer 9PLrJMMB6sl4qoSK8JPf8gy9mRVfvL"}
		data = {'model' : "food-items-v0.1", 'url' : imageURL}

		r = requests.get("https://api.clarifai.com/v1/tag/",headers = header,params=data)
		JSONTags = r.json()

		tagsData = JSONTags['results'][0]['result']['tag']
		tagList = zip(tagsData['classes'],tagsData['probs'])
		for tag in tagList:
			if tag[1] > .8:
				tagName = tag[0].encode()
				if not tagsDict.has_key(tagName):
					tagsDict[tagName] = 0
				tagsDict[tagName] += 1

	return tagsDict

def fourSearch(tagDict):
	clientID = 'JD5WEQCZLAOXXPVBYZV1TOUONBMWCUXNHCJALUSQN5YTUHKA'
	clientSecret = '1QW0UZYHRAVPJGCWA04JSJGHJ0RWEPW3XG3AF3GYJFUTYQRU'
	client = foursquare.Foursquare(client_id = clientID, client_secret= clientSecret)

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

print fourSearch({"Pizza" : 2, "Taco" : 1})

def restaurantRank(restaurantDict):
	return 0

def main():
##	imageURLs = getImageUrls("food")
	imageURLs = ['http://www.healthyfoodteam.com/wp-content/uploads/2014/02/Which-Food-You-Should-Never-Mix.jpg', 'http://travelchannel.sndimg.com/content/dam/images/travel/fullset/2014/08/20/63/food-paradise-106-burritos-ss-003', 'http://cdn.playbuzz.com/cdn/39f85817-18ad-4321-9908-03b342872b87/7838a2f8-fb2d-48e8-abc9-f7db942d3ede.jpg', 'http://travelchannel.sndimg.com/content/dam/images/travel/fullset/2015/03/24/bizarre-foods-delicious-destinations-112-hong-kong-ss/bizarre-foods-delicious-destinations-ss-038-hong-kong-typhoon-shelter-crab.jpg.rend.tccom.1280.960.jpeg', 'https://i.ytimg.com/vi/SeTpJNRnG6w/maxresdefault.jpg', 'http://d.fastcompany.net/multisite_files/fastcompany/imagecache/1280/poster/2015/01/3041647-poster-p-1-most-innovative-companies-2015-next-sectors-food.jpg', 'https://pixabay.com/static/uploads/photo/2015/07/30/18/23/burger-868145_960_720.jpg', 'https://i.ytimg.com/vi/JWsob3MZUQ4/maxresdefault.jpg', 'http://media4.popsugar-assets.com/files/2013/07/02/953/n/1922195/426ebedb72d4cbbd_taste-the-states-cover.xxxlarge/i/US-State-Foods.jpg', 'https://i.ytimg.com/vi/uDnd_C8Hkp8/maxresdefault.jpg']
	tags = getTags(imageURLs)
	print tags
	search = fourSearch(tags)
	print json.dumps(search, indent=4, sort_keys=True)

main()