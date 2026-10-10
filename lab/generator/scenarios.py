import random

TARGET_WIN = "192.168.122.197"
WINRM_USER = "Administrator"
WINRM_PASS = "Fitzsydden1001"  # ganti sesuai passwordmu

SCAN_PATHS = [
    "/admin", "/wp-admin", "/wp-login.php", "/phpmyadmin",
    "/.git/config", "/.env", "/backup", "/config.php.bak",
    "/../../../../etc/passwd", "/cgi-bin/", "/.well-known/security.txt",
    "/manager/html", "/actuator/health", "/.aws/credentials",
    "/server-status", "/console", "/debug", "/api/v1/users"
]

BRUTEFORCE_PASSWORDS = [
    "123456", "password", "admin123", "letmein", "qwerty123",
    "P@ssw0rd", "welcome1", "changeme", "root1234", "test1234"
]

BENIGN_USERNAMES = ["svc_backup", "jdoe", "mlee", "temp_contractor", "auditor01"]

def gen_scan_batch():
    """Case #5: scanning dengan subset path + user-agent acak"""
    n = random.randint(5, len(SCAN_PATHS))
    paths = random.sample(SCAN_PATHS, n)
    ua = random.choice([
        "Mozilla/5.0 (compatible; Nmap Scripting Engine)",
        "gobuster/3.6", "dirb 2.22", "python-requests/2.31"
    ])
    return {"paths": paths, "user_agent": ua}

def gen_bruteforce_batch():
    """Case #3: jumlah percobaan dan user target bervariasi"""
    n = random.randint(5, 15)
    target_user = random.choice(["Administrator", "Admin", "admin"])
    passwords = random.sample(BRUTEFORCE_PASSWORDS, min(n, len(BRUTEFORCE_PASSWORDS)))
    return {"target_user": target_user, "passwords": passwords}

def gen_user_creation():
    """Case #4: user yang dibuat lalu dihapus bervariasi"""
    username = random.choice(BENIGN_USERNAMES) + str(random.randint(100,999))
    return {"username": username}

def gen_app_error():
    """Case #2: event sintetis dengan source/pesan bervariasi"""
    sources = ["MyAppError", "LegacyAppCrash", "ServiceFaultSim"]
    return {"source": random.choice(sources), "event_id": random.choice([1000, 1001, 1026])}

def gen_benign_logon():
    """Baseline FP: logon wajar, bukan serangan"""
    return {"note": "benign logon via scheduled task simulation"}
