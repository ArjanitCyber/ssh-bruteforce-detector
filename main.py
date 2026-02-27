import re
import time
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

CONFIG_FILE = "config.json"
BLOCKED_FILE = "blocked_ips.json"
INCIDENT_LOG = "logs/incidents.log"

# Load config
with open(CONFIG_FILE) as f:
    config = json.load(f)

LOG_FILE = config["log_file"]
THRESHOLD = config["threshold"]
BAN_TIME = config["ban_time_seconds"]
WHITELIST = set(config["whitelist"])

ip_attempts = defaultdict(int)
blocked_ips = {}

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

def log_incident(message):
    with open(INCIDENT_LOG, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def save_blocked_ips():
    with open(BLOCKED_FILE, "w") as f:
        json.dump(blocked_ips, f)

def load_blocked_ips():
    global blocked_ips
    if os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE) as f:
            blocked_ips = json.load(f)

def block_ip(ip):
    if ip in WHITELIST:
        return

    print(f"[ALERT] Blocking IP: {ip}")
    log_incident(f"Blocked IP {ip} due to brute force")
    blocked_ips[ip] = (datetime.now() + timedelta(seconds=BAN_TIME)).isoformat()
    save_blocked_ips()

def unblock_expired_ips():
    now = datetime.now()
    expired = []

    for ip, expiry in blocked_ips.items():
        if now >= datetime.fromisoformat(expiry):
            expired.append(ip)

    for ip in expired:
        print(f"[INFO] Unblocking IP: {ip}")
        log_incident(f"Unblocked IP {ip}")
        del blocked_ips[ip]

    if expired:
        save_blocked_ips()

def monitor_logs():
    with open(LOG_FILE, "r") as file:
        file.seek(0, 2)  # Go to end (tail -f style)

        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue

            if "Failed password" in line:
                match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    ip = match.group(1)

                    if ip in blocked_ips:
                        continue

                    ip_attempts[ip] += 1
                    print(f"[DEBUG] {ip} failed attempt {ip_attempts[ip]}")

                    if ip_attempts[ip] > THRESHOLD:
                        block_ip(ip)

            unblock_expired_ips()

if __name__ == "__main__":
    print("=== SSH Brute Force Detector Started ===")
    load_blocked_ips()
    monitor_logs()
