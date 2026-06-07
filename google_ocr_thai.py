import os
import base64
import json
import requests

def ocr_thai_medicine_label(image_path, api_key=None):
    """
    ฟังก์ชันสำหรับทำ OCR ภาษาไทยจากรูปฉลากยา 
    โดยใช้ Google Cloud Vision API (ผ่าน API Key)
    """
    
    if not api_key:
        return "กรุณาใส่ API Key ของ Google Cloud Vision ในฟังก์ชัน"

    # 1. แปลงรูปภาพเป็น Base64
    try:
        with open(image_path, "rb") as image_file:
            content = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        return f"ไม่สามารถอ่านไฟล์ภาพได้: {e}"

    # 2. เตรียม Payload สำหรับส่งไป Google Cloud Vision
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    
    payload = {
        "requests": [
            {
                "image": {"content": content},
                "features": [
                    {"type": "DOCUMENT_TEXT_DETECTION"} # เหมาะสำหรับข้อความหนาแน่นแบบฉลากยา
                ],
                "imageContext": {
                    "languageHints": ["th", "en"] # ระบุว่ามีภาษาไทยและอังกฤษ
                }
            }
        ]
    }

    # 3. ส่ง Request
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # 4. ดึงข้อความออกมา
        if 'textAnnotations' in result['responses'][0]:
            full_text = result['responses'][0]['fullTextAnnotation']['text']
            return full_text
        else:
            return "ไม่พบข้อความในรูปภาพ"
            
    except Exception as e:
        return f"เกิดข้อผิดพลาดในการเรียก API: {e}"

if __name__ == "__main__":
    # --- ส่วนที่ต้องตั้งค่า ---
    MY_API_KEY = "YOUR_GOOGLE_CLOUD_VISION_API_KEY" # <--- ใส่ API Key ของคุณที่นี่
    IMAGE_TO_READ = "img_1.jpg" # ชื่อไฟล์รูปในเครื่องคุณ
    # -----------------------

    print(f"--- เริ่มต้นการอ่านฉลากยาจากไฟล์: {IMAGE_TO_READ} ---")
    
    if MY_API_KEY == "YOUR_GOOGLE_CLOUD_VISION_API_KEY":
        print("\n[คำแนะนำ] คุณยังไม่ได้ใส่ API Key")
        print("1. ไปที่: https://console.cloud.google.com/")
        print("2. เปิดใช้งาน Cloud Vision API")
        print("3. สร้าง API Key ในเมนู Credentials")
    else:
        text = ocr_thai_medicine_label(IMAGE_TO_READ, MY_API_KEY)
        print("\n--- ผลลัพธ์ที่ได้ ---")
        print(text)
