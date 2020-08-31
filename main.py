from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import pytesseract
from PIL import Image
import os

def ocr_jpn(filepath):
    filename = os.path.basename(filepath)
    print("読み込み画像: {}".format(filename))
    image = Image.open(filepath)
    return pytesseract.image_to_string(image, lang='jpn')  # print ocr text from image


app = Flask(__name__)

@app.route('/', methods=['get'])
def get():
    name = "Engineers"
    return render_template('index.html', title='flask test', name=name, flag=False)

@app.route('/', methods=['POST'])
def post():
    name = "Engineers"

    if request.method == 'POST':
        f = request.files.get('image')
        filepath = 'src/img/' + secure_filename(f.filename)
        f.save(filepath)

        result = ocr_jpn(filepath)
        os.remove(filepath)
    else:
        result == "ファイルが正しく選択されませんでした。"
    return render_template('index.html', title='flask test', name=name, result=result, flag=True)

@app.route('/test')
def good():
    name = "test"
    return name

if __name__ == "__main__":
    app.run(debug=True)
