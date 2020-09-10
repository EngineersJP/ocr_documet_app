# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response, jsonify
from werkzeug.utils import secure_filename

import pytesseract
from PIL import Image
import os

import base64
from io import BytesIO

import math
import cv2


available_ext = ['.png', '.jpeg', '.jpg']

class engineers_ocr(object):
    
    def __init__(self):
        
        print("Start OCR")

    def get_file_info(self, filename):
        filename_without_ext, ext = os.path.splitext(filename)
        filepath = 'src/img/' + filename
        return filename_without_ext, ext, filepath

    def get_rotation_minor_degree(self, filepath):
        # Use HoughLinesP to detect the lines and calculate the degree.
        img_before = cv2.imread(filepath)
        img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
        img_edges = cv2.Canny(img_gray, 100, 100, apertureSize = 3)
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength = 100, maxLineGap = 5)

        try:
            for x1, y1, x2, y2 in lines[0]:
                minor_degree = float(math.degrees(math.atan2(y2 - y1, x2 - x1)))
        except TypeError:
            minor_degree = 0
        minor_degree = minor_degree % 90
        print("Minor Degree: {}".format(minor_degree))

        return minor_degree

    def get_rotation_degree_by_quarter(self, image):
        # Use tesseract to calculate the degree.
        osd_info = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
        major_degree = osd_info['orientation']
        print("Major Degree: {}".format(major_degree))
                
        return major_degree


    def fix_dpi_and_rotation(self, image_for_rotate, filename, degrees, output_filepath):
        # adjust the orientation of the image
        image_transparency = image_for_rotate.convert("RGBA")
        print('{}を{}°修正しています...'.format(filename, degrees))

        image_rotated = image_transparency.rotate(degrees, expand = True)
        back_ground = Image.new("RGB", image_rotated.size, "white")
        back_ground.paste(image_rotated, (0, 0), image_rotated)
        image_pasted = back_ground.convert("RGB")
        
        image_pasted.save(output_filepath)
    
    def encode_image_to_bin(self, image):
        buf = BytesIO()
        image.save(buf, format="png")
        image_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
        image_b64data = "data:image/png;base64,{}".format(image_b64str)

        return image_b64data, image_b64str

    def main(self, filepath):
        filename = os.path.basename(filepath)  # xxx.jpg
        name = os.path.splitext(filename)[0]  # xxx
        output_filepath = "src/img/{}_rotated.jpg".format(name)
        print("読み込み画像: {}".format(filename))

        image = Image.open(filepath)

        minor_degree = self.get_rotation_minor_degree(filepath)
        if minor_degree:
            self.fix_dpi_and_rotation(image, filename, minor_degree, output_filepath)
        else:
            image.convert("RGB").save(output_filepath)

        image_output = Image.open(output_filepath)

        # get ocr text from image
        result = pytesseract.image_to_string(image_output, lang='jpn', config='--psm 1')
        major_degree = self.get_rotation_degree_by_quarter(image_output)

        if major_degree:
            self.fix_dpi_and_rotation(image_output, filename, major_degree, output_filepath)

        image_fixed_orientation = Image.open(output_filepath)
        total_degree = minor_degree + major_degree
        print("検出された角度: {}°".format(total_degree))
        result = result.replace(' ', '')
        os.remove(output_filepath)

        return image_fixed_orientation, result


app = Flask(__name__)


@app.route('/', methods=['get'])
def get():
    name = "ゲスト"
    return render_template(
        'index.html', title='OCR Document App',
        name=name, flag=False
    )


@app.route('/', methods=['POST'])
def post():
    name = "ゲスト"

    if request.method == 'POST':
        f = request.files.get('image')
        filename = secure_filename(f.filename)

        ocr_jpn = engineers_ocr()
        filename_without_ext, ext, filepath = ocr_jpn.get_file_info(filename)
        f.save(filepath)
        
        image, result = ocr_jpn.main(filepath)
        os.remove(filepath)

        image_b64data = ocr_jpn.encode_image_to_bin(image)[0]

    else:
        result == "ファイルが正しく選択されませんでした。"
    return render_template(
        'index.html', title='OCR Document App', name=name,
        image_b64data=image_b64data,
        filename_without_ext=filename_without_ext, result=result, flag=True
    )


@app.route('/test')
def good():
    name = "有効"
    return name

@app.route('/txt_download', methods=['POST'])
def txt_download():
    result = request.form['result']
    result = result.encode("utf-8")
    filename_without_ext = request.form['filename_without_ext']
    filename_without_ext = filename_without_ext.encode("utf-8").decode('iso-8859-1')
    return Response(
        result,
        mimetype='text/txt',
        headers={"Content-disposition":
                 "attachment; filename={}_result.txt".format(filename_without_ext)})

@app.route('/api', methods=['POST'])
def api():
    ocr_jpn = engineers_ocr()
    if 'image' in request.files:
        f = request.files.get('image')
        filename = secure_filename(f.filename)

        filename_without_ext, ext, filepath = ocr_jpn.get_file_info(filename)
        f.save(filepath)

        image, result = ocr_jpn.main(filepath)
        os.remove(filepath)

        image_b64str = ocr_jpn.encode_image_to_bin(image)[1]

    else:
        image = Image.open('static/img/engineers_ocr_logo.png')
        image_b64str = ocr_jpn.encode_image_to_bin(image)[1]
        result = "エラー: 対応するファイルを選択してください。"

    api_results = {
        'image': image_b64str,
        'result': result
    }

    return jsonify(api_results)

        

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html', code=500), 500

@app.errorhandler(503)
def internal_server_error(error):
    return render_template('internal_server_error.html', code=503), 503

if __name__ == "__main__":
    app.run(debug=True)
