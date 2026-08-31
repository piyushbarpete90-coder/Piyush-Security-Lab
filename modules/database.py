import sqlite3
from pathlib import Path
from datetime import datetime


DB_FILE = Path("data/security.db")
LOG_FILE = Path("logs/security.log")


def get_connection():
    DB_FILE.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_FILE)


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            target TEXT,
            details TEXT
        )
    """)

    connection.commit()
    connection.close()


def record_event(event_type, target="", details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events
        (timestamp, event_type, target, details)
        VALUES (?, ?, ?, ?)
    """, (timestamp, event_type, target, details))

    connection.commit()
    connection.close()


def add_event(timestamp, event_type, target="", details=""):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events
        (timestamp, event_type, target, details)
        VALUES (?, ?, ?, ?)
    """, (timestamp, event_type, target, details))

    connection.commit()
    connection.close()


def get_recent_events(limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, timestamp, event_type, target, details
        FROM events
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    connection.close()

    return rows


def show_database():
    rows = get_recent_events()

    print("\n===== 🗄️ DATABASE EVENTS =====")

    if not rows:
        print("❌ Database empty hai.")
        return

    for row in rows:
        event_id, timestamp, event_type, target, details = row

        print(
            f"[{event_id}] "
            f"{timestamp} | "
            f"{event_type} | "
            f"{target} | "
            f"{details}"
        )


def search_database():
    keyword = input("\n🔎 Enter search keyword: ").strip()

    if not keyword:
        print("❌ Keyword empty hai.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    pattern = f"%{keyword}%"

    cursor.execute("""
        SELECT id, timestamp, event_type, target, details
        FROM events
        WHERE timestamp LIKE ?
           OR event_type LIKE ?
           OR target LIKE ?
           OR details LIKE ?
        ORDER BY id DESC
    """, (pattern, pattern, pattern, pattern))

    rows = cursor.fetchall()
    connection.close()

    print("\n===== 🔎 SEARCH RESULTS =====")

    if not rows:
        print("❌ No matching events found.")
        return

    print(f"✅ Found: {len(rows)} event(s)\n")

    for row in rows:
        event_id, timestamp, event_type, target, details = row

        print(
            f"[{event_id}] "
            f"{timestamp} | "
            f"{event_type} | "
            f"{target} | "
            f"{details}"
        )


def database_stats():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE event_type LIKE '%DNS%'
    """)
    dns = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE event_type LIKE '%Port%'
    """)
    ports = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE event_type LIKE '%Banner%'
    """)
    banners = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE event_type LIKE '%HTTP%'
    """)
    http = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE details LIKE '%OPEN%'
    """)
    open_ports = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE details LIKE '%CLOSED%'
    """)
    closed_ports = cursor.fetchone()[0]

    connection.close()

    print("\n" + "=" * 45)
    print("        📊 DATABASE STATISTICS")
    print("=" * 45)

    print(f"📋 Total Events   : {total}")
    print(f"🌐 DNS Events     : {dns}")
    print(f"🔎 Port Events    : {ports}")
    print(f"🏷️ Banner Events  : {banners}")
    print(f"🌍 HTTP Events    : {http}")
    print(f"🟢 Open Ports     : {open_ports}")
    print(f"🔴 Closed Ports   : {closed_ports}")

    print("=" * 45)


def migrate_logs():
    init_database()

    if not LOG_FILE.exists():
        print("❌ security.log nahi mila.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    with LOG_FILE.open("r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    imported = 0

    for line in lines:
        if not line.startswith("[") or "] " not in line:
            continue

        timestamp, message = line.split("] ", 1)
        timestamp = timestamp[1:]

        if ":" in message:
            event_type, details = message.split(":", 1)
            event_type = event_type.strip()
            details = details.strip()
        else:
            event_type = "INFO"
            details = message

        cursor.execute("""
            INSERT INTO events
            (timestamp, event_type, target, details)
            VALUES (?, ?, ?, ?)
        """, (
            timestamp,
            event_type,
            "",
            details
        ))

        imported += 1

    connection.commit()
    connection.close()

    print("\n✅ Migration complete!")
    print(f"📥 Imported events: {imported}")
