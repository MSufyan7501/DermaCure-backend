
import cv2
from flask import Flask, request, jsonify,send_file
import os
import urllib.request
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
# app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Homepage'

def RemovingHair(fname):
    originalImg=cv2.imread(os.path.join("static","uploads",fname))
    greyScaleImg=cv2.imread(os.path.join("static","uploads",fname),0)

    filterSize = (17,17)
    kernel = cv2.getStructuringElement(1,filterSize)

    blackhat = cv2.morphologyEx(greyScaleImg, cv2.MORPH_BLACKHAT, kernel)
    ret, thresh2 = cv2.threshold(blackhat,10,255,cv2.THRESH_BINARY)

    dst = cv2.inpaint(originalImg,thresh2,1,cv2.INPAINT_TELEA)
    cv2.imwrite(os.path.join("static","uploads",fname),dst,[int(cv2.IMWRITE_JPEG_QUALITY), 90])


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'img' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('img')
     
    errors = {}
    success_resp={}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 501
        return resp
    if success:
        success_resp['filename'] = filename
        success_resp['url'] = "http://127.0.0.1:5000/static/uploads/" + filename
        resp = jsonify(success_resp)
        resp.status_code = 201
        RemovingHair(filename)
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 502
        return resp
@app.route('/clearedImg/<filename>', methods=['POST'])
def returnImg(filename):
    return send_file(f"static/uploads/{filename}")

if __name__ == '__main__':
    app.run(debug=True)