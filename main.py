import requests
import re
import socket
import base64
import json
from urllib.parse import urlparse

# منابع
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2RAY-CONFIGS/main/Warp-Lite",
    "https://t.me/s/v2ray_outlineir",
    "https://t.me/s/V2rayCollectorOfficial",
    "https://t.me/s/v2ray_free_conf",
    "https://raw.githubusercontent.com/Created-By/Telegram-Eag1e_YT/main/%40Eag1e_YT",
    "https://raw.githubusercontent.com/peweza/PUBLICSUB/refs/heads/main/PewezaVPNPubSUB",
    "https://t.me/s/v2ray_tk"
]

HEADERS = """#profile-title: base64:8J+UsFBld2V6YVZQTi1QdWJsaWMtU1VC
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=0
#profile-update-interval: 6

"""

def is_alive(config):
    """بررسی باز بودن پورت کانفیگ (تست سلامت ساده)"""
    try:
        if config.startswith("vmess://"):
            # دیکود کردن vmess برای پیدا کردن آدرس و پورت
            data = json.loads(base64.b64decode(config[8:]).decode('utf-8'))
            ip = data['add']
            port = int(data['port'])
        else:
            # برای vless, trojan, ss
            parsed = urlparse(config)
            ip = parsed.hostname
            port = parsed.port
        
        # تست اتصال به آی‌پی و پورت در ۲ ثانیه
        with socket.create_connection((ip, port), timeout=2):
            return True
    except:
        return False

def get_configs():
    configs = []
    for source in SOURCES:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                found = re.findall(r'(vless|vmess|trojan|ss|shadowsocks)://[^\s<>"\'#]+', response.text)
                for link in found:
                    # تمیز کردن لینک از کاراکترهای اضافه تلگرام
                    clean_link = re.split(r'[ \n\r\t<>]', link)[0]
                    if clean_link not in configs:
                        configs.append(clean_link)
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    return configs

def main():
    print("Fetching configs...")
    raw_configs = get_configs()
    print(f"Found {len(raw_configs)} configs. Testing health...")
    
    working_configs = []
    counter = 1
    
    for conf in raw_configs:
        if is_alive(conf):
            # حذف نام قدیمی و اضافه کردن CVP - 1
            base = conf.split('#')[0]
            working_configs.append(f"{base}#CVP - {counter}")
            counter += 1
            # محدودیت برای جلوگیری از طولانی شدن بیش از حد (اختیاری)
            if counter > 200: break 
    
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write(HEADERS)
        for conf in working_configs:
            f.write(conf + "\n")
            
    print(f"Finished! {len(working_configs)} healthy configs saved.")

if __name__ == "__main__":
    main()
