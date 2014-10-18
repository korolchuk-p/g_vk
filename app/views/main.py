from app import app
import json




@app.route('/test')
def test():
	return "+"



@app.route('/login', methods=['POST'])
def login():

    return json.dumps("{'success': 1}")

@app.route('/regist', methods=['POST'])
def regitration():

    return json.dumps("{'success': 1}")
