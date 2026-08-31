import socket
from modules.logger import log


def dns_lookup(host):
    try:
        ip = socket.gethostbyname(host)

        print(f"\n🌐 Host: {host}")
        print(f"📍 IP:   {ip}")

        log(f"DNS lookup: {host} -> {ip}")

    except socket.gaierror:
        print("❌ Host resolve nahi hua.")
        log(f"DNS lookup failed: {host}")


def network_menu():
    while True:
        print("\n===== 🌐 NETWORK TOOLS =====")
        print("1. DNS Lookup")
        print("2. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            host = input("Enter domain/hostname: ").strip()

            if host:
                dns_lookup(host)
            else:
                print("❌ Hostname empty hai.")

        elif choice == "2":
            break

        else:
            print("❌ Invalid choice.")
