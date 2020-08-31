from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import pytesseract
from PIL import Image
import os

import base64
from io import BytesIO

def ocr_jpn(filepath):
    filename = os.path.basename(filepath)
    print("読み込み画像: {}".format(filename))
    image = Image.open(filepath)
    result = pytesseract.image_to_string(image, lang='jpn')  # print ocr text from image
    return image, result


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

        image, result = ocr_jpn(filepath)
        os.remove(filepath)

        buf = BytesIO()
        image.save(buf,format="png")
        image_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
        image_b64data = "data:image/png;base64,{}".format(image_b64str)

    else:
        result == "ファイルが正しく選択されませんでした。"
    return render_template('index.html', title='flask test', name=name, image_b64data=image_b64data, result=result, flag=True)

@app.route('/test')
def good():
    name = "test"
    return name

if __name__ == "__main__":
    app.run(debug=True)
