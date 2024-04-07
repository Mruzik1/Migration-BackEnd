import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create a Flask application
app = Flask(__name__)

CORS(app)

# load environment variables

load_dotenv()

@app.post('/code_migrator')
def architector():
    # Check if the request contains JSON data
    if request.is_json:
        # Parse the JSON data from the request body
        data = request.get_json()
        # Access specific fields from the JSON data
        url = data.get('url')
        from_framwork = data.get('from_framwork')
        to_framwork = data.get('to_framework')
        
        # Perform processing based on the received data
        response = {
            'message': f'URL: {url}\n To: {to_framwork}, From: {from_framwork}'
        }
        # Return a JSON response
        return jsonify(response), 200
    else:
        return jsonify({'error': 'JSON error when reading user data'}), 400

# Run the app if executed directly
if __name__ == '__main__':
    app.run(
        host="localhost",
        port=os.getenv("FLASK_PORT", 6666), 
        debug=False
    )
