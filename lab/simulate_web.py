import requests
import time
import random

target = "http://192.168.122.197"

# === Case #5: Suspicious URL scanning ===
scan_paths = [
    "/admin", "/wp-admin", "/wp-login.php", "/phpmyadmin",
    "/.git/config", "/.env", "/backup", "/config.php.bak",
    "/../../../../etc/passwd", "/cgi-bin/", "/.well-known/security.txt",
    "/manager/html", "/actuator/health"
]
headers_scan = {"User-Agent": "Mozilla/5.0 (compatible; Nmap Scripting Engine)"}

print("=== Simulasi scanning (case #5) ===")
for path in scan_paths:
    try:
        r = requests.get(target + path, headers=headers_scan, timeout=3)
        print(f"{path} -> {r.status_code}")
    except Exception as e:
        print(f"{path} -> error: {e}")
    time.sleep(random.uniform(0.2, 1.0))

# === Case #1: Malformed request (HTTP 400) ===
print("\n=== Simulasi malformed request (case #1) ===")
try:
    r = requests.get(target + "/%", timeout=3)
    print(f"Malformed path -> {r.status_code}")
except Exception as e:
    print(f"Malformed request -> error: {e}")
