#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import edges
app = Flask(__name__)
picFolder=os.path.join("static",'pics')
app.config['UPLOAD_FOLDER']=picFolder
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def upload_image():
    imagefile=request.files['imagefile']
    image_path='C:\\Users\\Akshaya\\Downloads\\hned-20220911T044053Z-001\\hned\\images'+imagefile.filename
    imagefile.save(image_path)
    edges.fun(image_path)
    pic1=os.path.join(app.config['UPLOAD_FOLDER'],'canny_output1.jpg')
    pic=os.path.join(app.config['UPLOAD_FOLDER'],'input_output3.jpg')
    pic2=os.path.join(app.config['UPLOAD_FOLDER'],'hed_output2.jpg')
    return render_template('index.html',output=pic,output1=pic1,output2=pic2)
if __name__ == "__main__":
    app.run(debug=True)