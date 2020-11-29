from flask import Flask,request,jsonify
import os
import requests
import redis
import json
import datetime
import time
api = Flask(__name__)

@api.route('/api/messages',methods=['GET'])
def get_messages():
	response = requests.get('http://172.19.0.1:8080/')
	return response.content,response.status_code,response.headers.items()

if __name__ == "__main__":
	api.run()