from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")
