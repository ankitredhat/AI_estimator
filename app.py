from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Dummy multipliers for different containers (adjust these values based on your real data)
CONTAINER_MULTIPLIERS = {
    "Tawa": 0.8,
    "Kadhai": 1.0,
    "Patila": 1.2,
    "Dekchi": 1.1,
    "Handi": 1.3,
    "Drum": 2.0,
    "Tub": 1.5,
    "Thali": 0.7,
    "Katori": 0.5
}

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    container_type = data.get('container_type')
    length = float(data.get('length'))
    breadth = float(data.get('breadth'))

    if not container_type or not length or not breadth:
        return jsonify({'error': 'Missing required inputs'}), 400

    # Get multiplier for the selected container type
    multiplier = CONTAINER_MULTIPLIERS.get(container_type, 1.0)
    area_cm2 = length * breadth
    estimated_grams = min(max(int(area_cm2 * multiplier), 100), 5000)
    people_served = estimated_grams // 200  # Assuming 200g per person

    return jsonify({
        'container': container_type,
        'area': area_cm2,
        'estimated_quantity': f'{estimated_grams}g',
        'people_served': int(people_served)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render provides PORT env var
    app.run(host='0.0.0.0', port=port)
