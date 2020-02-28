# coding=utf8
from deeppavlov import build_model, configs
from werkzeug.utils import secure_filename
from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from flask_cors import CORS
from tika import parser
from waitress import serve
import json
import os
import time
import re


UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
model = None
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_pdf', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            json_response = {'paper': extract_text_from_pdf(file_path)}
            response = jsonify(json_response)
            return response
    return 'no ok'


@app.route('/ask_paper', methods=['POST'])
def ask_paper():
    if request.method == 'POST':
        json_string = request.get_json()
        data_dump = json.dumps(json_string)
        data = json.loads(data_dump)
        answer = model([data.get('paper')], [data.get('question')])[0]
        if not answer:
            answer = 'i dont know how to answer that, can you ask another question?'
        answer_json = {'answer': answer}
        response = jsonify(answer_json)
        return response


def extract_text_from_pdf(file_path):
    raw = parser.from_file(file_path)
    text = raw['content'].encode('ascii', 'ignore')
    text = text.decode('utf-8')
    one_line_text = str.join(" ", text.splitlines())
    one_line_text = one_line_text.replace('-', '')
    one_line_text = clean_pdf_text(one_line_text)
    return one_line_text


def clean_pdf_text(pdf_text):
    pdf_text = pdf_text.lower()
    pdf_text = pdf_text.split("abstract", 1)[1]
    pdf_text = pdf_text.split("references", 1)[0]
    pdf_text = pdf_text.replace(r"\(.*\)", "")
    pdf_text = re.sub(r'http\S+', '', pdf_text)
    pdf_text = re.sub("[\(\[].*?[\)\]]", "", pdf_text)
    return pdf_text


def setup_model():
    global model
    st = time.time()
    print("Loading model...")
    model = build_model(configs.squad.squad_bert_infer, download=True)
    print('loaded in: ', time.time() - st)


def main():
    setup_model()
    # extract_text_from_pdf('files/599.pdf')
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=False, host='0.0.0.0')


if __name__ == '__main__':
    main()
