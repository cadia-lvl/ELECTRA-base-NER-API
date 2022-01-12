from flask import Flask, request, jsonify, render_template, url_for
import mlflow.pyfunc
import pandas as pd
import requests

import json
import time
import string


app = Flask(__name__)

# Load in the model at app startup
model = mlflow.pyfunc.load_model('./model')


@app.route('/')
def home():
    return ""

@app.route("/predict", methods=['POST'])
def prediction():
    text = request.json
    print(text['text'])
    return predict(text['text'])

@app.route("/predict/impl", methods=['POST'])
def predict():

    params = request.args.to_dict()
    return predict(params['text'])

def predict(inp_text):
    text = pd.DataFrame(data={'text': [inp_text]})

    predictions = model.predict(text)
    return jsonify({"response":{
                    "type": "texts",
                    "content":predictions}})





@app.route("/headlines")
def headlines():
    return render_template("headlines.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
