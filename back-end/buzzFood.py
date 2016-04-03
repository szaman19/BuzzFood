import requests
import foursquare
import os

def getTags(imageURL):
	header = {'Authorization' : "Bearer 9PLrJMMB6sl4qoSK8JPf8gy9mRVfvL"}
	data = {'model' : "food-items-v0.1", 'url' : imageURL}

	r = requests.get("https://api.clarifai.com/v1/tag/",headers = header,params=data)
	JSONTags = r.json()

	tagsData = JSONTags['results'][0]['result']['tag']
	tagList = zip(tagsData['classes'],tagsData['probs'])
	tags = {}
	for tag in tagList:
		if tag[1] > .8:
			tags[tag[0]] = 1
	return tags

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

def restaurantRank(restaurantDict):
	return 0

def main():
    tags = getTags("http://www.flourarrangements.org/wp-content/uploads/2015/03/angel-food-cake-slice-with-chocolate-frosting-1.jpg")
    print tags
    print fourSearch(tags)

main()