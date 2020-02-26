from flask import Flask
import datetime

app = Flask(__name__)

@app.route("/time")
def get_current_time():
	return {'time': datetime.datetime.now()}
