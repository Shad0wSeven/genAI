#!/usr/bin/env python3 
import os, shutil
from catalogParser import *
from flask import send_from_directory

#yay a comment!

DELETE=False
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from format import *

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'fa'])



# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    if DELETE:
        folder = './uploads'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    errorCount, incorrectDicts = parser(debug=False)
    benign, dictOfVals = formatData(incorrectDicts)
    if len(dictOfVals) == 0:
        dictOfVals.append("You are not at risk of any diseases!")

    totalVariations = '{:,}'.format(benign)
    unmatcheds = '{:,}'.format(len(incorrectDicts))
    if errorCount > 20000:
        return render_template('failure.html')
    else:
        return render_template('results.html', filenames=filenames, totalVar=totalVariations, unmatched=unmatcheds, diseases=dictOfVals, incorrect=incorrectDicts)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404



@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )



# import os
# from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
# from werkzeug.utils import secure_filename
# from test import *
# from catalogParser import *

# UPLOAD_FOLDER = './uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'csv', 'fa', 'tsv'}

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     # parser()
#     # return send_from_directory(app.config['UPLOAD_FOLDER'],
#     #                            filename)
#     return render_template('results.html', totalVar="73,425", potHarmVar="394", unmatched="12332", listed="8<br>7<br>6", diseases="1<br>2<br>3<br>")
#     # VERY MESSY!



# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             # return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return render_template('index.html')
#     # return '''
#     # <!doctype html>
#     # <title>Upload new File</title>
#     # <h1>Upload new File</h1>
#     # <form method=post enctype=multipart/form-data>
#     #   <input type=file name=file>
#     #   <input type=submit value=Upload>
#     # </form>
#     # '''
