import requests
import re
import socket
import base64
import json
from urllib.parse import urlparse

# منابع ارسالی شما و منابع کمکی
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

def is_alive(config):
    """تست سلامت پورت کانفیگ"""
    try:
        host, port = None, None
        if config.startswith("vmess://"):
            v_data = config[8:].split('#')[0]
            # اصلاح پدینگ برای دیکود کردن صحیح
            missing_padding = len(v_data) % 4
            if missing_padding: v_data += '=' * (4 - missing_padding)
            decoded = json.loads(base64.b64decode(v_data).decode('utf-8'))
            host, port = decoded.get('add'), decoded.get('port')
        else:
            parsed = urlparse(config)
            host, port = parsed.hostname, parsed.port
        
        if host and port:
            # تست اتصال با زمان ۳ ثانیه
            with socket.create_connection((host, int(port)), timeout=3):
                return True
    except:
        pass
    return False

def get_configs():
    all_links = []
    # رگکس اصلاح شده برای گرفتن کل لینک (استفاده از ?: برای عدم ایجاد گروه)
    pattern = r'(?:vless|vmess|trojan|ss|shadowsocks|tuic|hysteria2|hy2)://[^\s<>"\'|]+'
    
    for source in SOURCES:
        try:
            print(f"در حال بررسی منبع: {source}")
            res = requests.get(source, timeout=20)
            if res.status_code == 200:
                content = res.text
                
                # اگر کل متن بیس۶۴ باشد، آن را دیکود کن
                if "://" not in content:
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                found = re.findall(pattern, content)
                print(f"تعداد {len(found)} کانفیگ پیدا شد.")
                all_links.extend(found)
        except Exception as e:
            print(f"خطا در دریافت: {e}")
            
    return list(set(all_links)) # حذف تکراری‌ها

def main():
    raw_configs = get_configs()
    print(f"کل کانفیگ‌های منحصر به فرد: {len(raw_configs)}")
    
    final_list = []
    counter = 1
    
    for conf in raw_configs:
        # حذف نام قبلی اگر وجود داشت
        base_link = conf.split('#')[0]
        
        # بررسی سلامت
        if is_alive(base_link):
            final_list.append(f"{base_link}#CVP - {counter}")
            counter += 1
            print(f"سالم: CVP - {counter-1}")
        
        if counter > 300: break # محدودیت برای سرعت

    # اگر تستی موفق نبود (برای اینکه فایل خالی نماند)
    if not final_list and raw_configs:
        for conf in raw_configs[:30]:
            base_link = conf.split('#')[0]
            final_list.append(f"{base_link}#CVP - {counter}")
            counter += 1

    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write(HEADERS)
        for c in final_list:
            f.write(c + "\n")
            
    print(f"پایان! {len(final_list)} کانفیگ در فایل ذخیره شد.")

if __name__ == "__main__":
    main()
