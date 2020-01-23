import json
from flask import Flask, request, render_template, jsonify
import cmath
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

client = pymongo.MongoClient("mongodb+srv://heroku-app:7653heroku@cluster0-krokl.mongodb.net/test?retryWrites=true&w=majority")
db = client["mydatabase"]
col = db["coefficients"]

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")

@app.route("/request", methods = ['POST'])
def getRequest():
	if request.method == "POST":
		a = request.form["A"]
		b = request.form["B"]
		c = request.form["C"]
		a = float(a)
		b = float(b)
		c = float(c)

		coef = { "a":str(a), "b":str(b), "c":str(c)}
		res = col.insert_one(coef)

		d = (b**2) - (4*a*c)
		if d < 0:
		    return "This equation has no real solution"
		elif d == 0:
		    x = (-b)/(2*a)
		    return "This equation has one solutions: " + str(x.real)
		else:
		    x1 = (-b-cmath.sqrt(d))/(2*a)
		    x2 = (-b+cmath.sqrt(d))/(2*a)
		    return "This equation has two solutions: " + str(x1.real) + ", " + str(x2.real)

@app.route("/API", methods = ['GET'])
def apiGET():
	r = col.find()
	l = list(r)
	return dumps(l)

@app.route("/API", methods = ['POST'])
def apiPOST():
	a = request.json["A"]
	b = request.json["B"]
	c = request.json["C"]
	coef = { "a":a, "b":b, "c":c}
	res = col.insert_one(coef)
	return jsonify({"response":"successfully added"})

@app.route("/API", methods = ['PUT'])
def apiPUT():
	a = request.json["A"]
	b = request.json["B"]
	c = request.json["C"]
	coef = { "a":a, "b":b, "c":c}
	res = col.update_one({'_id':ObjectId(str(request.json["_id"]))}, {"$set": coef}, upsert=True)
	return jsonify({"response":"successfully updated"})

@app.route("/API", methods = ['DELETE'])
def apiDELETE():
	res = col.delete_one({'_id':ObjectId(str(request.json["_id"]))})
	return jsonify({"response":"successfully deleted"})

if __name__ == '__main__':
	app.run(debug=True)