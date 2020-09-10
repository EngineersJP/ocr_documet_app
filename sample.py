import requests
import json

import cv2
import base64
import numpy as np

url = "https://engineers-ocr.herokuapp.com//api"
files = { "image": open('src/img/image.png', 'rb') }

image_path = "src/img/image.jpg"

r = requests.post(url, files=files)
print('httpレスポンス: {}'.format(r))

r = r.json()

# OCRの結果を標準出力
print(r['result'])

## 角度補正済みの画像データをローカルに保存
img_base64 = r['image']

# RAWデータをjpgに変換
img_binary = base64.b64decode(img_base64)
jpg=np.frombuffer(img_binary,dtype=np.uint8)

img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
cv2.imwrite(image_path,img)

#表示確認
cv2.imshow('window title', img)
cv2.waitKey(0)
cv2.destroyAllWindows()