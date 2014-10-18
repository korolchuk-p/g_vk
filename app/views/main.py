from app import app
import json
from flask import Flask, render_template



@app.route('/test')
def test():
	return "+"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    return json.dumps("{'success': 1}")

@app.route('/regist', methods=['POST'])
def regitration():

    return json.dumps("{'success': 1}")
