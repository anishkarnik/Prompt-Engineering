from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define the API endpoint for image generation
IMAGE_GENERATION_API = "https://api.monsterapi.ai/v1/generate/sdxl-base"
BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjVkZWYwNDZkODVjMmM5ODA2ZDJiNTk2MzZjNWZjMjk5IiwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTNUMDg6MzM6MjIuMjQxMDU5In0.g5SEtFWiFAkrvSfVjVCkN2wM-72Psf4lKsPuOLYgWcg"  # Replace this with your actual bearer token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_images', methods=['POST'])
def generate_images():
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

    # Extract process ID from the response headers
    process_id = response.headers.get('process_id')

    # Return the response from the image generation API along with the process ID
    return jsonify({
        'images': response.json(),
        'process_id': process_id
    })

@app.route('/fetch_process_id', methods=['GET'])
def fetch_process_id(process_id):
    process_id = response.json(process_id)
    url = "https://api.monsterapi.ai/v1/status/{process_id}"

    headers = {"accept": "application/json", "Authorization": f"Bearer {BEARER_TOKEN}"}

    response = requests.get(url, headers=headers)

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)