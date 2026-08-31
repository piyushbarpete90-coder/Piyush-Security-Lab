import hashlib
import os


def calculate_sha256(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def integrity_menu():
    while True:
        print("\n" + "=" * 40)
        print("🛡️ PIYUSH FILE INTEGRITY LAB")
        print("=" * 40)
        print("1. Calculate SHA-256")
        print("2. Compare SHA-256")
        print("3. Back")
        print("=" * 40)

        choice = input("Choose: ").strip()

        if choice == "1":
            filepath = input("Enter file path: ").strip()

            if not os.path.isfile(filepath):
                print("❌ File not found.")
                continue

            try:
                result = calculate_sha256(filepath)
                print("\nSHA-256:")
                print(result)
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "2":
            filepath = input("Enter file path: ").strip()

            if not os.path.isfile(filepath):
                print("❌ File not found.")
                continue

            expected = input("Enter original SHA-256: ").strip().lower()

            try:
                actual = calculate_sha256(filepath)

                if actual == expected:
                    print("✅ FILE INTEGRITY OK")
                    print("File has not changed.")
                else:
                    print("⚠️ FILE CHANGED")
                    print("SHA-256 does not match.")

            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "3":
            break

        else:
            print("❌ Invalid choice.")
