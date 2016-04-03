from flask import Flask, request, g, jsonify
import os, json
app = Flask(__name__)
@app.route('/query')
def returnListOfImages():
    returnArray = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9_x4IhsaCSKSsnjrtfX920IpOsU2fGktKUGICSf0Bio13WvCAITy2NOgx",\
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWJWbrqRHY4_KJVdYVxd4PvHzRqFjZInhDy1NDRcslhCM3QLObWIBb4fz7",\
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHhW_JNH2I6A1XmeDv29KhyiYCjlIbZZqUvmMVoDsDcvT1E05FgXLcqBs"\
    ]
    return jsonify(result=returnArray)

if __name__ == '__main__':
    app.run(debug=True)
