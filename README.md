# OCR Documet App

# 開発環境
### macOS:
```
macOS Mojave 10.14.6
Python 3.8.5
virtualenv 20.0.10
tesseract 4.1.1
```
# 環境設定
## データセットの用意
tesseract-ocrの[tessdata](https://github.com/tesseract-ocr/tessdata)をzipでダウンロードし、`usr⁩/local⁩/Cellar⁩/tesseract⁩/⁨<バージョン数>/⁩`配下に保存してください。  
*)高精度モデルは[こちら](https://github.com/tesseract-ocr/tessdata_best)から
## macOS
まず、TesseractをHomebrewでインストールします。
```
$ brew install tesseract --HEAD
```
下記の要領で`virtual env`を設定してください。 
```
$ cd ocr_document_app
$ virtualenv -p python3.8.5 .
```

`virtual env`を設定したら、以下のコマンドで仮想環境を起動し、必要なライブラリを全てインストールしてください。
```
$ source bin/activate
(ocr_document_app)$ pip install -r requirements.txt
```
全てのライブラリをインストールできたか確認してください。
```
(ocr_document_app)$ pip list
```

作業を終了するたびに仮想環境を停止するのを忘れないでください。
```
(ocr_document_app)$ deactivate
$
```
# 実行方法
仮想環境が立ち上がっていることを確認してください。
```
$ python main.py
```
でFlaskを起動します。
