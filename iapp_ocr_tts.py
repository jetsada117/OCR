import requests
import json
import os
from gtts import gTTS
import pygame
import time


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
    # ตรวจสอบว่าถ้า text เป็น list ให้รวมเป็น string เดียวกันก่อน
    if isinstance(text, list):
        text = " ".join(text)

    # แทนที่ \n (ขึ้นบรรทัดใหม่) ด้วยเว้นวรรค เพื่อให้เสียงอ่านต่อเนื่องกัน
    if text:
        text = text.replace("\n", " ")

    if not text or text.startswith("เกิดข้อผิดพลาด") or text == "ไม่พบข้อความในรูปภาพ":
        print("ไม่มีข้อความให้อ่านออกเสียง")
        return

    try:
        print("\nกำลังแปลงข้อความเป็นเสียง...")
        # 1. สร้างเสียงโดยใช้ gTTS (Google Text-to-Speech)
        tts = gTTS(text=text, lang="th")
        filename = "ocr_voice.mp3"
        tts.save(filename)

        # 2. เล่นเสียงโดยใช้ pygame
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        print("กำลังเล่นเสียง... (กด Ctrl+C เพื่อหยุด)")
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.mixer.quit()
        # ลบไฟล์ชั่วคราวหลังจากเล่นจบ (optional)
        # os.remove(filename)

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเล่นเสียง: {e}")


if __name__ == "__main__":
    # --- ส่วนที่ต้องตั้งค่า ---
    MY_IAPP_KEY = (
        "iapp_live_1e1599dcefdf16db1805f0df538e17c402dc5d2879445c4a9af4d426c1d12138"
    )
    IMAGE_PATH = "img_3.jpg"  # ไฟล์รูปของคุณ
    # -----------------------

    print(f"--- 1. เริ่มต้นการ OCR ภาพ: {IMAGE_PATH} ---")

    ocr_result = iapp_thai_ocr(IMAGE_PATH, MY_IAPP_KEY)

    print("\n--- 2. ผลลัพธ์ OCR ภาษาไทย ---")
    print(ocr_result)

    print("\n--- 3. เริ่มการอ่านออกเสียง (Text-to-Speech) ---")
    speak_thai(ocr_result)
