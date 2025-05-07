from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    try:
        image = Image.open(image_file.stream)
    except Exception as e:
        return jsonify({'error': f'Invalid image: {str(e)}'}), 400

    width, height = image.size
    area = width * height

    # Dummy logic for estimation
    estimated_grams = min(max(area // 1000, 100), 1000)  # 100g–1000g
    people_served = estimated_grams // 200  # Assuming 200g/person

    return jsonify({
        'estimated_quantity': f'{estimated_grams}g',
        'people_served': int(people_served)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render provides PORT env var
    app.run(host='0.0.0.0', port=port)
