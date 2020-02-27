from deeppavlov import build_model, configs
from werkzeug.utils import secure_filename
from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from flask_cors import CORS
import json
from pdfminer import high_level
import os
import time

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
        answer = {'answer': model([data.get('paper_text')], [data.get('question')])[0]}
        response = jsonify(answer)
        return response


def extract_text_from_pdf(file_path):
    text = high_level.extract_text(file_path)
    one_line_text = str.join(" ", text.splitlines())
    one_line_text = one_line_text.replace('-', '')
    return one_line_text


def setup_model():
    global model
    st = time.time()
    print("Loading model...")
    model = build_model(configs.squad.squad_bert_infer, download=True)
    print('loaded in: ', time.time() - st)


def main():
    setup_model()
    app.run(debug=False)


if __name__ == '__main__':
    main()