from flask import Flask,request,jsonify
import os
import requests
import json
import datetime
import time
api = Flask(__name__)
redis_client =  redis.Redis()

@api.route('/api/messages',methods=['GET'])
def get_messages():
	response = requests.get('http://host.docker.internal:8080/')
	return response.content,response.status_code,response.headers.items()


	
if __name__ == "__main__":
	api.run()