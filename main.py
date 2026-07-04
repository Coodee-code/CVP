import requests
import re
import socket
import base64
import json
from urllib.parse import urlparse

# منابع ارسالی شما + منابع کمکی معتبر
SOURCES = [
    "https://raw.githubusercontent.com/Created-By/Telegram-Eag1e_YT/main/%40Eag1e_YT",
    "https://raw.githubusercontent.com/peweza/PUBLICSUB/refs/heads/main/PewezaVPNPubSUB",
    "https://raw.githubusercontent.com/barry-far/V2RAY-CONFIGS/main/Warp-Lite",
    "https://t.me/s/v2ray_outlineir",
    "https://t.me/s/V2rayCollectorOfficial",
    "https://t.me/s/v2ray_free_conf",
    "https://t.me/s/v2ray_tk"
]

HEADERS = """#profile-title: base64:8J+UsFBld2V6YVZQTi1QdWJsaWMtU1VC
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=0
#profile-update-interval: 6

"""

def is_alive(config):
    """تست سریع باز بودن پورت برای اطمینان از زنده بودن سرور"""
    try:
        host, port = None, None
        if config.startswith("vmess://"):
            data = config[8:].split('#')[0]
            # اصلاح پدینگ بیس64
            missing_padding = len(data) % 4
            if missing_padding: data += '=' * (4 - missing_padding)
            decoded = json.loads(base64.b64decode(data).decode('utf-8'))
            host, port = decoded.get('add'), decoded.get('port')
        else:
            parsed = urlparse(config)
            host, port = parsed.hostname, parsed.port
        
        if host and port:
            with socket.create_connection((host, int(port)), timeout=2):
                return True
    except:
        pass
    return False

def get_configs():
    unique_configs = set()
    # شناسایی انواع پروتکل‌ها: vmess, vless, trojan, ss, tuic, hysteria2
    pattern = r'(vless|vmess|trojan|ss|shadowsocks|tuic|hysteria2|hy2)://[^\s<>"\'|]+'
    
    for source in SOURCES:
        try:
            print(f"در حال دریافت از: {source}")
            res = requests.get(source, timeout=15)
            if res.status_code == 200:
                # اگر منبع خودش بیس64 شده باشد (مثل برخی ساب‌ها)
                content = res.text
                try:
                    # تست برای دیکود کردن کل فایل اگر بیس64 بود
                    decoded_content = base64.b64decode(content).decode('utf-8')
                    content = decoded_content
                except:
                    pass
                
                found = re.findall(pattern, content)
                for link in found:
                    # تمیزکاری نهایی لینک
                    clean_link = link.split('#')[0].split('"')[0].split("'")[0]
                    unique_configs.add(clean_link)
        except Exception as e:
            print(f"خطا در منبع {source}: {e}")
            
    return list(unique_configs)

def main():
    raw_configs = get_configs()
    print(f"تعداد کل کانفیگ‌های یافت شده: {len(raw_configs)}")
    
    final_list = []
    counter = 1
    
    for conf in raw_configs:
        # تست سلامت (می‌توانید برای دریافت تمام کانفیگ‌ها این شرط if را بردارید)
        if is_alive(conf):
            # تغییر نام به CVP - 1, ...
            # در پروتکل‌های مدرن مثل hy2 و tuic نام در انتهای لینک بعد از # است
            final_list.append(f"{conf}#CVP - {counter}")
            counter += 1
            if counter > 500: break # محدودیت برای جلوگیری از سنگین شدن ساب
            
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write(HEADERS)
        for c in final_list:
            f.write(c + "\n")
            
    print(f"عملیات موفقیت‌آمیز: {len(final_list)} کانفیگ سالم ذخیره شد.")

if __name__ == "__main__":
    main()
