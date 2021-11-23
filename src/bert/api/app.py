from flask import Flask, request, jsonify, render_template, url_for
from in_docker import translate_path
import mlflow.pyfunc
import pandas as pd
from multiprocessing import Process

# import docker
import tempfile

import requests

import json
import time
import string
import os

app = Flask(__name__)

# Load in the models at app startup
model1 = mlflow.pyfunc.load_model('./model1')
model2 = mlflow.pyfunc.load_model('./model2')
model3 = mlflow.pyfunc.load_model('./model3')
model4 = mlflow.pyfunc.load_model('./model4')
print('-=-=-Models initialized-=-=-')
# docker_client = docker.from_env()
print('-=-=-Docker client initialized-=-=-')


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    params = request.args.to_dict()

    text = pd.DataFrame(data={'text': [params['text']]})

    predictions = model1.predict(text)

    if request.method == 'GET':
        return add_html_tags(predictions)

    if request.method == 'POST':
        return jsonify([predictions])

    return ''


def predict_model1(text, folder_name):
    print('MODEL1')
    annotated_text = model1.predict_for_conllfile(text)
    save_annotated_to_file(annotated_text, folder_name, "first_file")


def predict_model2(text, folder_name):
    print('MODEL2')
    annotated_text = model2.predict_for_conllfile(text)
    save_annotated_to_file(annotated_text, folder_name, "second_file")


def predict_model3(text, folder_name):
    print('MODEL3')
    annotated_text = model3.predict_for_conllfile(text)
    save_annotated_to_file(annotated_text, folder_name, "third_file")


def predict_model4(text, folder_name):
    print('MODEL4')
    annotated_text = model4.predict_for_conllfile(text)
    save_annotated_to_file(annotated_text, folder_name, "fourth_file")


def save_annotated_to_file(text, folder_name, model_name):
    with open("{}/{}".format(folder_name, model_name), "w") as text_file:
        text_file.write(text)


@app.route('/predict_ensamble', methods=['POST'])
def predict_ensamble():
    if 'file' not in request.files:
        return ''
    file = request.files['file'].read()
    text = file.decode("utf-8")
    if not text[-2:] == '\n\n':
        text += '\n'

    # temp_dir = tempfile.TemporaryDirectory()
    # temp_dir_name = temp_dir.name
    # absolute_temp_dir_path = translate_path(temp_dir_name)

    preds1 = model1.predict_for_conllfile(text)
    preds2 = model2.predict_for_conllfile(text)
    preds3 = model3.predict_for_conllfile(text)
    preds4 = model4.predict_for_conllfile(text)

    print('model1 output length : {}'.format(len(preds1)))
    print('model2 output length : {}'.format(len(preds2)))
    print('model3 output length : {}'.format(len(preds3)))
    print('model4 output length : {}'.format(len(preds4)))
    # # os.system('docker run -it --rm -v {}/:/Data asmundur1/combitagger:4taggers'.format(absolute_temp_dir_path))
    # # os.system(
    # #     "awk -v OFS='\t' 'NR>1{{ print $1, $NF }}' {0}/output.txt > {0}/filtered_output.txt".format(temp_dir_name))
    #
    # with open(temp_dir_name + '/' + 'filtered_output.txt', 'r') as file:
    #     output_text = file.read()

    return preds1


@app.route('/predict_conll', methods=['GET', 'POST'])
def predict_conll():
    if 'file' not in request.files:
        return ''
    file = request.files['file'].read()
    proper_file = file.decode("utf-8")
    if not proper_file[-2:] == '\n\n':
        proper_file += '\n'

    conll_string = model1.predict_for_conllfile(proper_file)
    return conll_string


@app.route("/headlines")
def headlines():
    return render_template("headlines.html")


def add_html_tags(predictions):
    html_text = ''
    for i, (token, label) in enumerate(zip(*predictions)):
        if token in ['[CLS]', '[SEP]']:
            continue
        if token[:2] == '##':
            token = token[2:]
        elif token in string.punctuation:
            pass
        else:
            token = f" {token}"
        if label != 'O':
            html_text += f"<span class='{label.lower()}' title='{label}'>{token} </span>"
        else:
            html_text += f"{token}"

    return html_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
