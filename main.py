from modules.logger import log, analyze_logs
from modules.network import network_menu
from modules.scanner import scanner_menu
from modules.http_tools import http_menu
from modules.database import (
    init_database,
    show_database,
    search_database,
    database_stats
)
from modules.hash_tools import hash_menu
from modules.integrity_tools import integrity_menu


def show_menu():
    print("\n" + "=" * 45)
    print("      🛡️ PIYUSH SECURITY LAB v1")
    print("=" * 45)
    print("1. 🌐 Network Tools")
    print("2. 🔎 Scanner Tools")
    print("3. 🌍 HTTP Tools")
    print("4. 📊 Log Analyzer")
    print("5. 🗄️ Database Events")
    print("6. 🔍 Database Search")
    print("7. 📈 Database Statistics")
    print("8. 🔐 Hash Lab")
    print("9. 🛡️ File Integrity Lab")
    print("10. ❌ Exit")
    print("=" * 45)


def main():
    init_database()
    log("Security Lab launched")

    while True:
        show_menu()

        choice = input("Choose: ").strip()

        if choice == "1":
            network_menu()

        elif choice == "2":
            scanner_menu()

        elif choice == "3":
            http_menu()

        elif choice == "4":
            analyze_logs()

        elif choice == "5":
            show_database()

        elif choice == "6":
            search_database()

        elif choice == "7":
            database_stats()

        elif choice == "8":
            hash_menu()

        elif choice == "9":
            integrity_menu()

        elif choice == "10":
            log("Security Lab closed")
            print("\n👋 Bye!")
            break

        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
