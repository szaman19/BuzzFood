import requests
import json

def getImageUrls(query):
    cx = "018347742159790243558:yjmlvg2ulxg"
    q = query
    key = "AIzaSyBNWmypZhvryr_CUmVfJ8h1NLqWdfyIJDA"
    searchType = "image"

    params = {
        "key": key,
        "cx" : cx,
        "q":q,
        "searchType":searchType
    }
    url = "https://www.googleapis.com/customsearch/v1"

    r = requests.get(url,params=params)

    jsonDump = json.dumps(r.json())

    items = json.loads(jsonDump)

    print json.dumps(items, indent=4, sort_keys=True)

def main():
    getImageUrls("Food")
main()
