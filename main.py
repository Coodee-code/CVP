import requests
import re
import socket
import base64
import json
import binascii
from urllib.parse import urlparse

# منابع ارسالی شما و منابع معتبر دیگر
SOURCES = [
    "https://raw.githubusercontent.com/Created-By/Telegram-Eag1e_YT/main/%40Eag1e_YT",
    "https://raw.githubusercontent.com/peweza/PUBLICSUB/refs/heads/main/PewezaVPNPubSUB",
    "https://raw.githubusercontent.com/barry-far/V2RAY-CONFIGS/main/Warp-Lite",
    "https://t.me/s/v2ray_outlineir",
    "https://t.me/s/V2rayCollectorOfficial"
]

HEADERS = """#profile-title: base64:8J+UsFBld2V6YVZQTi1QdWJsaWMtU1VC
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=0
#profile-update-interval: 6

"""

def safe_base64_decode(data):
    """دیکود کردن ایمن بیس ۶۴"""
    try:
        data = data.strip()
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8')
    except:
        return None

def is_alive(config):
    """بررسی اتصال به سرور (تایم‌اوت ۳ ثانیه)"""
    try:
        host, port = None, None
        if config.startswith("vmess://"):
            v_data = config[8:].split('#')[0]
            decoded = json.loads(safe_base64_decode(v_data))
            host, port = decoded.get('add'), decoded.get('port')
        else:
            parsed = urlparse(config)
            host, port = parsed.hostname, parsed.port
        
        if host and port:
            with socket.create_connection((host, int(port)), timeout=3):
                return True
    except:
        pass
    return False

def get_configs():
    unique_configs = set()
    # شناسایی تمام پروتکل‌های V2Ray
    pattern = r'(vless|vmess|trojan|ss|shadowsocks|tuic|hysteria2|hy2)://[^\s<>"\'|]+'
    
    for source in SOURCES:
        try:
            print(f"Checking: {source}")
            res = requests.get(source, timeout=20)
            if res.status_code == 200:
                content = res.text
                
                # مرحله اول: اگر کل فایل بیس۶۴ است، دیکودش کن
                decoded = safe_base64_decode(content)
                if decoded:
                    content = decoded
                
                # مرحله دوم: پیدا کردن لینک‌ها در متن (چه دیکود شده چه خام)
                found = re.findall(pattern, content)
                print(f"--- Found {len(found)} configs in this source.")
                for link in found:
                    # حذف اضافات
                    clean_link = link.split('#')[0].split('"')[0].strip()
                    unique_configs.add(clean_link)
        except Exception as e:
            print(f"Error in {source}: {e}")
            
    return list(unique_configs)

def main():
    raw_configs = get_configs()
    total_found = len(raw_configs)
    print(f"Total Unique Configs Found: {total_found}")
    
    final_list = []
    counter = 1
    
    for conf in raw_configs:
        # اگر می‌خواهید تمام کانفیگ‌ها را بگیرید و تست سلامت را حذف کنید،
        # خط زیر را بردارید و فقط بخش اضافه کردن به لیست را بگذارید.
        if is_alive(conf):
            final_list.append(f"{conf}#CVP - {counter}")
            counter += 1
            if counter > 500: break
    
    # اگر هیچ کانفیگ سالمی پیدا نشد (برای جلوگیری از خالی ماندن فایل)
    # ۵ تا از اولین کانفیگ‌ها را بدون تست سلامت اضافه کن
    if not final_list and raw_configs:
        print("No healthy configs found! Adding some raw configs as fallback...")
        for conf in raw_configs[:20]:
            final_list.append(f"{conf}#CVP - {counter} (Unverified)")
            counter += 1

    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write(HEADERS)
        for c in final_list:
            f.write(c + "\n")
            
    print(f"Final Report: {len(final_list)} configs saved.")

if __name__ == "__main__":
    main()
