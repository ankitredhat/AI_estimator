from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from math import pi
import os

app = Flask(__name__, static_folder='static')
CORS(app)

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

def calculate_volume(container_type, length, breadth):
    radius = length / 2
    default_height = 5  # cm

    if container_type in ["Tawa", "Thali", "Katori"]:
        height = default_height
        return pi * (radius ** 2) * height
    elif container_type in ["Kadhai", "Dekchi", "Handi", "Patila", "Drum", "Tub"]:
        height = breadth
        return pi * (radius ** 2) * height
    else:
        return 0

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    container_type = data.get('container_type')
    length = float(data.get('length'))
    breadth = float(data.get('breadth'))
    unit = data.get('unit', 'cm')

    if not container_type or not length or not breadth:
        return jsonify({'error': 'Missing required inputs'}), 400

    if unit == 'm':
        length *= 100
        breadth *= 100

    volume_cm3 = calculate_volume(container_type, length, breadth)
    multiplier = CONTAINER_MULTIPLIERS.get(container_type, 1.0)
    estimated_grams = min(max(int(volume_cm3 * multiplier), 100), 5000)
    people_served = estimated_grams // 200

    return jsonify({
        'container': container_type,
        'volume_cm3': round(volume_cm3, 2),
        'estimated_quantity': f'{estimated_grams}g',
        'people_served': int(people_served)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
