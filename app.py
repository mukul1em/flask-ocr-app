from flask import Flask,render_template,request,url_for
from ocr_core import ocr_core
import os

app=Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def upload_page():
    if request.method=='POST':
         #check if the post request has the file part

        if 'file' not in request.files:
            return render_template('index.html',msg='No file selected')
        file=request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename=='':
            return render_template('index.html',msg='No file selected')
        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            extracted_text = ocr_core(file)
            return render_template('index.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)

    elif request.method == 'GET':
        return render_template('index.html')












if __name__=='__main__':
    app.run(debug=True)