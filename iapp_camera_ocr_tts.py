import cv2
import requests
import json
import os
from gtts import gTTS
import pygame
import time


def capture_image(output_filename="captured_label.jpg"):
    """
    ฟังก์ชันสำหรับเปิดกล้องและถ่ายภาพ
    กด Space เพื่อถ่ายภาพ, กด ESC เพื่อยกเลิก
    """
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("ไม่สามารถเปิดกล้องได้")
        return None

    cv2.namedWindow("Camera - Press SPACE to Capture, ESC to Exit")

    img_counter = 0
    captured_path = None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("ไม่สามารถรับภาพจากกล้องได้")
            break

        cv2.imshow("Camera - Press SPACE to Capture, ESC to Exit", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("ยกเลิกการถ่ายภาพ")
            break
        elif k % 256 == 32:
            # SPACE pressed
            captured_path = output_filename
            cv2.imwrite(captured_path, frame)
            print(f"ถ่ายภาพสำเร็จ: {captured_path}")
            break

    cam.release()
    cv2.destroyAllWindows()
    return captured_path


def iapp_thai_ocr(image_path, api_key):
    """
    ฟังก์ชันสำหรับทำ OCR ภาษาไทยโดยใช้ iApp Technology API (v3)
    """
    url = "https://api.iapp.co.th/v3/store/ocr/document/ocr"
    headers = {"apikey": api_key}

    try:
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(url, headers=headers, files=files)

            if response.status_code != 200:
                return (
                    f"เกิดข้อผิดพลาดจาก API ({response.status_code}): {response.text}"
                )

            result = response.json()
            if "text" in result:
                return result["text"]
            else:
                return "ไม่พบข้อความในรูปภาพ"

    except Exception as e:
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}"


def speak_thai(text):
    """
    ฟังก์ชันสำหรับแปลงข้อความเป็นเสียงภาษาไทย และเล่นเสียง
    """
    if isinstance(text, list):
        text = " ".join(text)

    if text:
        text = text.replace("\n", " ")

    if not text or text.startswith("เกิดข้อผิดพลาด") or text == "ไม่พบข้อความในรูปภาพ":
        print("ไม่มีข้อความให้อ่านออกเสียง")
        return

    try:
        print("\nกำลังแปลงข้อความเป็นเสียง...")
        tts = gTTS(text=text, lang="th")
        filename = "ocr_voice.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        print("กำลังเล่นเสียง... (กด Ctrl+C เพื่อหยุด)")
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)

        pygame.mixer.quit()

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเล่นเสียง: {e}")


if __name__ == "__main__":
    # --- ส่วนที่ต้องตั้งค่า ---
    MY_IAPP_KEY = (
        "iapp_live_5a9f03703184b1e83a409c5394d2e69ce790cddb835b9ba73c32a21093d6d210"
    )
    # -----------------------

    print("--- 1. เปิดกล้องเพื่อถ่ายภาพฉลากยา ---")
    image_path = capture_image()

    if image_path and os.path.exists(image_path):
        print(f"\n--- 2. เริ่มต้นการ OCR ภาพ: {image_path} ---")
        ocr_result = iapp_thai_ocr(image_path, MY_IAPP_KEY)

        print("\n--- 3. ผลลัพธ์ OCR ภาษาไทย ---")
        print(ocr_result)

        print("\n--- 4. เริ่มการอ่านออกเสียง (Text-to-Speech) ---")
        speak_thai(ocr_result)
    else:
        print("ไม่ได้ถ่ายภาพ โปรแกรมจบการทำงาน")
