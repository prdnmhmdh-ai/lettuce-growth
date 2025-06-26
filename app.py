import os
import base64
from flask import Flask, send_from_directory, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient
from PIL import Image
from io import BytesIO

app = Flask(__name__, static_folder='assets')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="zHXvPR4wY6HIpFlHqkFg"
)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/detect", methods=["GET"])
def detect_page():
    return render_template("detect.html")

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        if 'camera_image' in data:
            data_url = data['camera_image']
            header, encoded = data_url.split(",", 1)
            binary_data = base64.b64decode(encoded)
            image = Image.open(BytesIO(binary_data))

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'camera_capture.jpg')
            image.save(image_path, optimize=True, quality=75)

        elif 'image' in request.files:
            file = request.files['image']
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)

        else:
            return jsonify({"reply": "❌ No image provided"}), 400

        result = CLIENT.infer(image_path, model_id="aquaponic_polygan_test/2")

        print("Full model response:", result)

        return jsonify(result)

    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
