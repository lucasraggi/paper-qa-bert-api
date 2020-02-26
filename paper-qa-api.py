from deeppavlov import build_model, configs
from werkzeug.utils import secure_filename
from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import url_for
from waitress import serve
import pdfplumber
import json
import PyPDF2
from pdfminer import high_level
import os

UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
model = None
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_pdf', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('oi')
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
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    return 'no ok'


def extract_text_from_pdf(file_path):
    text = high_level.extract_text(file_path)
    one_line_text = str.join(" ", text.splitlines())
    one_line_text = one_line_text.replace('-', '')
    return one_line_text


def setup_model():
    global model
    print("Loading model...")
    model = build_model(configs.squad.squad_bert)
    input_text = 'The U.S. is ready to engage in talks about North Korea’s nuclear program even as it maintains pressure on Kim Jong Un’s regime, the Washington Post reported, citing an interview with Vice President Mike Pence. Pence and South Korea’s President Moon Jae-in agreed on a post-Olympics strategy during conversations at the Winter Olympics in the South Korean resort of Pyeongchang that Pence dubbed “maximum pressure and engagement at the same time.” Pence spoke in an interview on his way home from the Winter Olympics. “The point is, no pressure comes off until they are actually doing something that the alliance believes represents a meaningful step toward denuclearization,” the Post quoted Pence as saying. “So the maximum pressure campaign is going to continue and intensify. But if you want to talk, we’ll talk.”'
    print(model([input_text], ['What country is under the pressure?']))


def main():
    # setup_model()
    # serve(app, host='0.0.0.0', port=5000)
    app.run(debug=False)


if __name__ == '__main__':
    main()