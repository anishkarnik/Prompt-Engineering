from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import os

app = Flask(__name__)
# Define the upload folder
UPLOAD_FOLDER = 'D:/react_for_TechFest/assests_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "chatgpt"
DB_USER = "postgres"
DB_PASS = "ezwq2173"

# Establish a database connection
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

# Define the API endpoint for image generation
IMAGE_GENERATION_API = "https://api.edenai.run/v2/image/generation"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjNjYmIxM2QtYTMzOC00ODNhLWFkNzgtYmI3Nzc0YTQwNTBhIiwidHlwZSI6ImFwaV90b2tlbiJ9.w4vXBtpZ3tFJaP7S3ErIQkHjUt3WZNFQs76cuoGjhoc"  # Replace this with your actual bearer token

# Define your login route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data = request.form
            username = data['username']
            email = data['email']
            lab = data['lab']
            
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('INSERT INTO users (username, email, lab) VALUES (%s, %s, %s)',
                        (username, email, lab))
            conn.commit()
            cur.close()
            conn.close()
            
            # Redirect to the image generation page after successful login
            return redirect('/generate_image')
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    else:
        return render_template('index.html')

# Define the image generation route
@app.route('/generate_image', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'POST':
        data = request.json

        # Prepare data for the API call
        payload = {
            "text": data.get('text', ''),
            "resolution": data.get('resolution', ''),
            "providers": data.get('providers', ''),  # Handle the case where 'providers' might not exist
            "fallback_providers": data.get('fallback_providers', '')
        }

        # Set up headers with the bearer token
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Make a request to the image generation API
        response = requests.post(IMAGE_GENERATION_API, json=payload, headers=headers)

        # Return the response from the image generation API
        return jsonify(response.json())
    else:
        return render_template('generate_image.html')

# Define the endpoint and function for handling the image upload
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded file to the upload folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
