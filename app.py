from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import base64
import os
import io

app = Flask(__name__)
CORS(app)

# --- ส่วนที่ต้องตั้งค่า ---
MY_IAPP_KEY = (
    "iapp_live_5a9f03703184b1e83a409c5394d2e69ce790cddb835b9ba73c32a21093d6d210"
)
# -----------------------


def iapp_thai_ocr_from_base64(base64_image, api_key):
    """ส่งรูปภาพ Base64 ไปประมวลผลที่ iApp"""
    url = "https://api.iapp.co.th/v3/store/ocr/document/ocr"
    headers = {"apikey": api_key}

    try:
        # ตัดส่วน header ของ base64 ออก (ถ้ามี) เช่น data:image/jpeg;base64,
        if "," in base64_image:
            base64_image = base64_image.split(",")[1]

        image_data = base64.b64decode(base64_image)
        image_file = io.BytesIO(image_data)

        files = {"file": ("image.jpg", image_file, "image/jpeg")}
        response = requests.post(url, headers=headers, files=files)

        if response.status_code != 200:
            return f"Error: {response.status_code}"

        result = response.json()
        if "text" in result:
            text = result["text"]
            if isinstance(text, list):
                text = " ".join(text)
            return text.replace("\n", " ")
        else:
            return "ไม่พบข้อความ"

    except Exception as e:
        return f"Error connecting to iApp: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    if not data or "image" not in data:
        return jsonify({"error": "No image data"}), 400

    result_text = iapp_thai_ocr_from_base64(data["image"], MY_IAPP_KEY)
    return jsonify({"text": result_text})


if __name__ == "__main__":
    # รันบนพอร์ต 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
