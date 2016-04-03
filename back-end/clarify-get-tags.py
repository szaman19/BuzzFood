import requests
import os

def getTags(imageURL):
    data = {}
    data['model'] = "food-items-v0.1"
    data['url'] = imageURL
    header = {}
    header['Authorization'] = "Bearer 9PLrJMMB6sl4qoSK8JPf8gy9mRVfvL"
    r = requests.get("https://api.clarifai.com/v1/tag/",headers = header,params=data)
    JSONTags = r.json()
    tags = JSONTags['results'][0]['result']['tag']
    zipped = zip(tags['classes'],tags['probs'])
    return zipped

def intersection(tagsList):
    listIntersection = []
    return listIntersection

def main():
    print getTags("http://www.flourarrangements.org/wp-content/uploads/2015/03/angel-food-cake-slice-with-chocolate-frosting-1.jpg")
main()
