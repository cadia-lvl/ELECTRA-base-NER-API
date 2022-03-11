from flask import Flask, request, jsonify, render_template, url_for
import mlflow.pyfunc
import pandas as pd
import requests

import traceback
import json
import time
import string


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False 

# Load in the model at app startup
model = mlflow.pyfunc.load_model('./model')

def error(errors):
	return jsonify({"failure":{"errors":[errors]}})

def human_readable_output(label):
	if label == "O":
		return "Outside"
	if label[:2] == "I-":
		return "Inside-"+label[2:]
	if label[:2] == "B-":
		return "Beginning-"+label[2:]
	return "Unknown-"+label

@app.route('/')
def home():
	return ""

@app.route("/predict", methods=['POST'])
def prediction():
	text = ""
	try:
		text = request.json
	except:
		return error({"code":"ner.json", "text":"The input could not be parsed into json", "detail":{'traceback':traceback.format_exc()}})
	
	try:
		df = pd.DataFrame(data={"text":[text["content"]]})
	except:
		return error({"code":"ner.missing.content", "text":"There is no content in the input", "detail":{'traceback':traceback.format_exc()}})

	try:
		prediction, ner = model.predict(df)
		start, end = 0,0
		label = ""
		cur = False
		annotations = {}
		for i, _ner in enumerate(ner):
			if (_ner[:2] == "B-" or _ner == "O") and cur:
				end = i
				if label not in annotations:
					annotations[label] = []
				annotations[label].append({"start":start, "end":end})
				cur = False
			if _ner[:2] == "B-":
				cur = True
				label = _ner[2:]
				start = i	
		
		return jsonify({"response":{
					"type": "texts",
					"texts":[{
						"role":"segment",
						"texts":[{
							"content":pred,
							"features":{
								"ner":human_readable_output(_ner)
							}} 
							for pred,_ner in zip(prediction,ner)],
							"annotations":annotations
							}]
						}})
							
	except:
		return error({"code":"ner.model", "text":"Error response from model", "detail":{'traceback':traceback.format_exc()}})


@app.route("/headlines")
def headlines():
	return render_template("headlines.html")


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
