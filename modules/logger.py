from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/security.log")


def log(message):
    LOG_FILE.parent.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def read_logs():
    if not LOG_FILE.exists():
        return []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def analyze_logs():
    logs = read_logs()

    print("\n===== 📊 LOG ANALYZER =====")

    if not logs:
        print("❌ No logs found.")
        return

    total = len(logs)

    open_ports = sum("OPEN" in line for line in logs)
    closed_ports = sum("CLOSED" in line for line in logs)
    http_checks = sum("HTTP check:" in line for line in logs)
    dns_checks = sum("DNS lookup:" in line for line in logs)

    print(f"📋 Total Entries : {total}")
    print(f"🟢 Open Ports    : {open_ports}")
    print(f"🔴 Closed Ports  : {closed_ports}")
    print(f"🌍 HTTP Checks   : {http_checks}")
    print(f"🌐 DNS Lookups   : {dns_checks}")

    print("\n===== 🕒 RECENT ACTIVITY =====")

    for entry in logs[-5:]:
        print(entry)
