from flask import Flask, request, g, jsonify, make_response, current_app
import os, json, requests
from datetime import timedelta
from functools import update_wrapper
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['GET'])

def returnListOfImages():
    query = request.args['query']
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
    print(imageUrlDict)
    return jsonify(results=imageUrlDict)
    #
    # returnArray = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9_x4IhsaCSKSsnjrtfX920IpOsU2fGktKUGICSf0Bio13WvCAITy2NOgx",\
    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWJWbrqRHY4_KJVdYVxd4PvHzRqFjZInhDy1NDRcslhCM3QLObWIBb4fz7",\
    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHhW_JNH2I6A1XmeDv29KhyiYCjlIbZZqUvmMVoDsDcvT1E05FgXLcqBs"\
    # ]
    # print(request.args['query'])
    # returnArray.append(request.args['query'])
    # return jsonify(result=returnArray)
@app.route('/imageTags',methods=['GET'])
def getImageTag():
    imageUrls = request.args['urls']
    print(imageUrls)
    print(type(imageUrls))
    return "Working"


if __name__ == '__main__':
    app.run(debug=True)
