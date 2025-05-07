from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from math import pi
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

# Function to calculate area/volume based on shape
def calculate_area_or_volume(container_type, length, breadth):
    if container_type == "Tawa" or container_type == "Kadhai":
        # Assuming it's a circular container (Tawa/Kadhai are round)
        radius = length / 2  # Assuming length is the diameter
        return pi * (radius ** 2)  # Area of circle
    elif container_type == "Patila":
        # Assuming Patila is a cylinder, so volume calculation
        radius = length / 2  # Assuming length is diameter
        height = breadth  # Considering breadth as height here
        return pi * (radius ** 2) * height  # Volume of cylinder
    elif container_type in ["Dekchi", "Handi", "Thali"]:
        # Assuming shallow cylinder
        radius = length / 2  # Assuming length is diameter
        return pi * (radius ** 2)  # Area of shallow cylinder
    elif container_type in ["Drum", "Tub"]:
        # Assuming deep cylinder
        radius = length / 2  # Assuming length is diameter
        height = breadth  # Considering breadth as height here
        return pi * (radius ** 2) * height  # Volume of deep cylinder
    elif container_type == "Katori":
        # Assuming Katori is a small shallow bowl-like container
        radius = length / 2  # Assuming length is diameter
        return pi * (radius ** 2)  # Area of circle
    else:
        return 0  # Default case if container type is not recognized

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    container_type = data.get('container_type')
    length = float(data.get('length'))
    breadth = float(data.get('breadth'))
    unit = data.get('unit', 'cm')  # Default to centimeters

    if not container_type or not length or not breadth:
        return jsonify({'error': 'Missing required inputs'}), 400

    # Convert to centimeters if unit is meter
    if unit == 'm':
        length *= 100
        breadth *= 100

    # Calculate area/volume based on container shape
    area_or_volume = calculate_area_or_volume(container_type, length, breadth)

    # Get multiplier for the selected container type
    multiplier = CONTAINER_MULTIPLIERS.get(container_type, 1.0)

    # Estimate grams based on area/volume
    estimated_grams = min(max(int(area_or_volume * multiplier), 100), 5000)

    # Calculate the number of people served (assuming 200g per person)
    people_served = estimated_grams // 200

    return jsonify({
        'container': container_type,
        'area_or_volume': area_or_volume,
        'estimated_quantity': f'{estimated_grams}g',
        'people_served': int(people_served)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render provides PORT env var
    app.run(host='0.0.0.0', port=port)

