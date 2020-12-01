from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def server_log():
	if os.path.exists('/data/app/log.txt'):
		return send_from_directory('/data/app',filename='log.txt')
	else:
		return '',200


if __name__ == "__main__":
	app.run()
