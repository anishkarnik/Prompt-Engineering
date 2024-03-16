import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Path to the directory containing images
IMAGE_DIRECTORY = r'D:/image generater/Tx/my_flask_app/static/images'

@app.route('/')
def index():
    # Get a list of image filenames in the directory
    images = os.listdir(IMAGE_DIRECTORY)
    # Render the HTML template and pass the list of images to it
    return render_template('index.html', images=images)

@app.route('/images/<path:filename>')
def serve_image(filename):
    # Serve images from the specified directory
    return send_from_directory(IMAGE_DIRECTORY, filename)

if __name__ == '__main__':
    app.run(debug=True)
