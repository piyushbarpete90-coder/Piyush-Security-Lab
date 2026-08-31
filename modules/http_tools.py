import time
import urllib.request
import urllib.error

from modules.logger import log


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def http_checker():
    print("\n===== 🌍 HTTP CHECKER =====")

    url = input("Enter URL: ").strip()

    if not url:
        print("❌ URL empty hai.")
        return

    url = normalize_url(url)

    print(f"\n🔗 URL: {url}")
    print("🔍 Checking...")

    start = time.perf_counter()

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "PiyushSecurityLab/1.0"}
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            elapsed = (time.perf_counter() - start) * 1000

            status = response.status
            server = response.headers.get("Server", "Unknown")
            content_type = response.headers.get(
                "Content-Type",
                "Unknown"
            )

            print(f"✅ Status Code: {status}")
            print(f"⚡ Response Time: {elapsed:.2f} ms")
            print(f"🖥️ Server: {server}")
            print(f"📄 Content-Type: {content_type}")

            log(
                f"HTTP check: {url} | "
                f"status={status} | "
                f"time={elapsed:.2f}ms"
            )

    except urllib.error.HTTPError as error:
        elapsed = (time.perf_counter() - start) * 1000

        print(f"⚠️ HTTP Error: {error.code}")
        print(f"⚡ Response Time: {elapsed:.2f} ms")

        log(f"HTTP error: {url} | status={error.code}")

    except urllib.error.URLError as error:
        print(f"❌ Connection failed: {error.reason}")
        log(f"HTTP connection failed: {url}")

    except Exception as error:
        print(f"❌ Error: {error}")
        log(f"HTTP checker error: {url}")


def http_menu():
    while True:
        print("\n===== 🌍 HTTP TOOLS =====")
        print("1. HTTP Checker")
        print("2. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            http_checker()

        elif choice == "2":
            break

        else:
            print("❌ Invalid choice.")
