import requests
import base64
import json


def iapp_thai_ocr(image_path, api_key):
    """
    ฟังก์ชันสำหรับทำ OCR ภาษาไทยโดยใช้ iApp Technology API (v3)
    """
    # อัปเดต URL เป็นเวอร์ชันล่าสุดที่รองรับ General OCR
    url = "https://api.iapp.co.th/v3/store/ocr/document/ocr"

    headers = {"apikey": api_key}

    try:
        # 1. ส่งไฟล์ภาพ (iApp ใช้ชื่อ parameter ว่า 'file')
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(url, headers=headers, files=files)

            # 2. ตรวจสอบสถานะ
            if response.status_code != 200:
                return (
                    f"เกิดข้อผิดพลาดจาก API ({response.status_code}): {response.text}"
                )

            result = response.json()

            # 3. ดึงข้อความ (iApp v3 มักคืนค่าเป็น 'text' หรือผลลัพธ์โดยตรง)
            if "text" in result:
                return result["text"]
            else:
                return json.dumps(result, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}"


if __name__ == "__main__":
    # --- ส่วนที่ต้องตั้งค่า ---
    # สมัครสมาชิกที่ https://iapp.co.th เพื่อรับ API Key
    MY_IAPP_KEY = (
        "iapp_live_1e1599dcefdf16db1805f0df538e17c402dc5d2879445c4a9af4d426c1d12138"
    )
    IMAGE_PATH = "img_3.jpg"  # ไฟล์รูปของคุณ
    # -----------------------

    print(f"--- กำลังส่งภาพ {IMAGE_PATH} ไปประมวลผลที่ iApp Technology ---")

    if MY_IAPP_KEY == "YOUR_IAPP_API_KEY":
        print("\n[!] กรุณาใส่ API Key ก่อนใช้งาน")
        print("วิธีรับ Key:")
        print("1. เข้าไปที่ https://iapp.co.th/ และสมัครสมาชิก")
        print("2. ไปที่เมนู API หรือ Dashboard")
        print("3. คัดลอก API Key มาวางในตัวแปร MY_IAPP_KEY")
    else:
        output = iapp_thai_ocr(IMAGE_PATH, MY_IAPP_KEY)
        print("\n--- ผลลัพธ์ OCR ภาษาไทย ---")
        print(output)
