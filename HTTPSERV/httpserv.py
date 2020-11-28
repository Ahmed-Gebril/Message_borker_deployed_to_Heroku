from flask import Flask,send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def server_log():
	return send_from_directory('/usr/data','log.txt')

if __name__ == "__main__":
	app.run()