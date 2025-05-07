from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import math

app = Flask(__name__, static_folder='static')
CORS(app)

# Volume formulas by container (assuming cylindrical or hemispherical shape)
CONTAINER_SHAPES = {
    "Tawa": "flat_cylinder",
    "Kadhai": "hemisphere",
    "Patila": "cylinder",
    "Dekchi": "cylinder",
    "Handi": "deep_bowl",
    "Drum": "cylinder",
    "Tub": "cylinder",
    "Thali": "flat_cylinder",
    "Katori": "bowl"
}

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    container_type = data.get('container_type')
    diameter = float(data.get('diameter'))
    height = float(data.get('height'))

    if not container_type or not diameter or not height:
        return jsonify({'error': 'Missing inputs'}), 400

    radius = diameter / 2

    shape = CONTAINER_SHAPES.get(container_type, 'cylinder')
    volume_cm3 = 0

    if shape == "cylinder":
        volume_cm3 = math.pi * radius**2 * height
    elif shape == "hemisphere":
        volume_cm3 = (2/3) * math.pi * radius**3
    elif shape == "flat_cylinder":
        volume_cm3 = math.pi * radius**2 * (height * 0.3)
    elif shape == "bowl":
        volume_cm3 = (2/3) * math.pi * radius**2 * height
    elif shape == "deep_bowl":
        volume_cm3 = (3/4) * math.pi * radius**2 * height
    else:
        volume_cm3 = math.pi * radius**2 * height  # fallback

    estimated_grams = min(max(int(volume_cm3 * 0.85), 100), 5000)
    people_served = estimated_grams // 200

    return jsonify({
        'container': container_type,
        'volume_cm3': round(volume_cm3, 2),
        'estimated_quantity': f'{estimated_grams}g',
        'people_served': people_served
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
