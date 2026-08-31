import hashlib


def hash_text():
    print("\n🔐 HASH GENERATOR")
    print("-" * 40)

    text = input("Enter text: ")

    sha256 = hashlib.sha256(text.encode()).hexdigest()
    sha512 = hashlib.sha512(text.encode()).hexdigest()

    print("\nSHA-256:")
    print(sha256)

    print("\nSHA-512:")
    print(sha512)


def verify_sha256():
    print("\n🔎 SHA-256 VERIFIER")
    print("-" * 40)

    text = input("Enter original text: ")
    expected = input("Enter SHA-256 hash: ").strip().lower()

    actual = hashlib.sha256(text.encode()).hexdigest()

    if actual == expected:
        print("✅ Hash MATCH")
    else:
        print("❌ Hash does NOT match")


def hash_menu():
    while True:
        print("\n" + "=" * 40)
        print("🔐 PIYUSH HASH LAB")
        print("=" * 40)
        print("1. Generate SHA-256 / SHA-512")
        print("2. Verify SHA-256")
        print("3. Back")
        print("=" * 40)

        choice = input("Choose: ").strip()

        if choice == "1":
            hash_text()

        elif choice == "2":
            verify_sha256()

        elif choice == "3":
            break

        else:
            print("❌ Invalid choice.")
