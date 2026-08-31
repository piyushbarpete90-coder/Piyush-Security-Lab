import socket

from modules.logger import log


def check_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((host, port))
        sock.close()

        return result == 0

    except socket.error:
        return False


def port_checker():
    print("\n===== 🔎 PORT CHECKER =====")

    host = input("Enter IP/Host: ").strip()

    if not host:
        print("❌ Host empty hai.")
        return

    try:
        port = int(input("Enter Port: ").strip())

        if not 1 <= port <= 65535:
            print("❌ Port 1-65535 ke beech hona chahiye.")
            return

    except ValueError:
        print("❌ Invalid port.")
        return

    print("\n🔍 Checking...")

    if check_port(host, port):
        print(f"✅ Port {port} is OPEN")
        log(f"Port check: {host}:{port} OPEN")
    else:
        print(f"❌ Port {port} is CLOSED")
        log(f"Port check: {host}:{port} CLOSED")


def banner_grabber():
    print("\n===== 🏷️ BANNER GRABBER =====")

    host = input("Enter IP/Host: ").strip()

    if not host:
        print("❌ Host empty hai.")
        return

    try:
        port = int(input("Enter Port: ").strip())

        if not 1 <= port <= 65535:
            print("❌ Invalid port.")
            return

    except ValueError:
        print("❌ Invalid port.")
        return

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        print("\n🔌 Connecting...")
        sock.connect((host, port))

        try:
            sock.sendall(b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n")
        except socket.error:
            pass

        data = sock.recv(2048)
        sock.close()

        if data:
            banner = data.decode("utf-8", errors="replace").strip()

            print("\n📡 Server Response:")
            print("-" * 45)
            print(banner)
            print("-" * 45)

            log(f"Banner grabbed: {host}:{port}")
        else:
            print("⚠️ Server ne response nahi diya.")

    except ConnectionRefusedError:
        print("❌ Connection refused. Port open nahi hai.")

    except socket.timeout:
        print("⏱️ Connection timed out.")

    except OSError as error:
        print(f"❌ Connection error: {error}")


def scanner_menu():
    while True:
        print("\n===== 🔎 SCANNER TOOLS =====")
        print("1. Port Checker")
        print("2. Banner Grabber")
        print("3. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            port_checker()

        elif choice == "2":
            banner_grabber()

        elif choice == "3":
            break

        else:
            print("❌ Invalid choice.")
