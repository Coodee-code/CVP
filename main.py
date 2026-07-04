import requests
import re
import base64
import os

# تنظیمات
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2RAY-CONFIGS/main/Warp-Lite", # نمونه لینک ساب
    "https://t.me/s/v2ray_outlineir", # نمونه کانال تلگرام (نمای وب)
    "https://t.me/s/V2rayCollectorOfficial",
    "https://raw.githubusercontent.com/Created-By/Telegram-Eag1e_YT/main/%40Eag1e_YT"
]

HEADERS = """#profile-title: base64:8J+UsFBld2V6YVZQTi1QdWJsaWMtU1VC
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=0
#profile-update-interval: 6

"""

def get_configs():
    configs = []
    for source in SOURCES:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                # استخراج لینک‌های کانفیگ با Regex
                found = re.findall(r'(vless|vmess|trojan|ss|shadowsocks)://[^\s<>"]+', response.text)
                for link in found:
                    # اگر لینک در تلگرام بود و کاراکترهای اضافی داشت پاکسازی شود
                    full_link = re.findall(r'(vless|vmess|trojan|ss|shadowsocks)://[^\s<>"]+', response.text)
                    configs.extend(full_link)
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    return list(set(configs)) # حذف تکراری‌ها

def rename_configs(configs):
    renamed = []
    for i, config in enumerate(configs, 1):
        # حذف نام قبلی (هر چیزی بعد از #)
        if "#" in config:
            base = config.split("#")[0]
        else:
            base = config
        
        # افزودن نام جدید CVP - 1, ...
        new_config = f"{base}#CVP - {i}"
        renamed.append(new_config)
    return renamed

def main():
    raw_configs = get_configs()
    # در اینجا می‌توانید سیستم چک کردن سلامت (Health Check) ساده اضافه کنید
    # اما برای سرعت بالا، فعلاً فقط فرمت‌های صحیح را نگه می‌داریم
    
    final_configs = rename_configs(raw_configs)
    
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write(HEADERS)
        for conf in final_configs:
            f.write(conf + "\n")
    print(f"Successfully saved {len(final_configs)} configs.")

if __name__ == "__main__":
    main()
