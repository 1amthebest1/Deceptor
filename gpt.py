import requests
import sys
import time

# --------------------------------------------------
print("")
print("##################*+*##########*#**###*****#########**############")
print("#......-#.....**......+#.....#:.....:=.....-*...#*...:..##...#..:%")
print("#..:#...#...*##-..=*..:#...###:..+=..##:..+##...#-..+=..=#...+..:%")
print("#..:#...#.....#-..=*==+#.....#:..-...##:..+##...#:..+=..=#......:%")
print("#..:#...#...++#-..=#***#...++#:..--+###:..+##...#:..+=..=#..-...:%")
print("#..:#...#...*##=..=*..:#...###:..+#####:..+##...#-..+=..=#..*...:%")
print("#......:#.....=#.:....*#.....+:..+#####:..+##...#*......##..**..:%")
print("%%%%#########################################################%%%%%")
print("")

# ---------------- GLOBALS ----------------

TOTAL_REQUESTS = 0
RATE_LIMIT = 0
REQUESTS_THIS_SECOND = 0
LAST_TICK = time.time()

# ---------------- HELPERS ----------------

def askPermission():
    if input("Do you want to start? (Y/N): ").lower() != 'y':
        sys.exit(0)

def rate_limit():
    global REQUESTS_THIS_SECOND, LAST_TICK

    REQUESTS_THIS_SECOND += 1
    elapsed = time.time() - LAST_TICK

    if elapsed < 1 and REQUESTS_THIS_SECOND >= RATE_LIMIT:
        time.sleep(1 - elapsed)
        REQUESTS_THIS_SECOND = 0
        LAST_TICK = time.time()
    elif elapsed >= 1:
        REQUESTS_THIS_SECOND = 0
        LAST_TICK = time.time()

def load_headers():
    headers = {}
    with open("headers.txt", "r") as f:
        for line in f:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
    return headers

# ---------------- CORE ----------------

def requestSender(url):
    global TOTAL_REQUESTS

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            cookies=COOKIES,
            allow_redirects=False,
            timeout=10
        )
    except requests.RequestException:
        return

    TOTAL_REQUESTS += 1
    rate_limit()

    # ---- STATUS CHECK ----
    if str(r.status_code) != STATUS_CODE:
        return

    # ---- MATCHER EXCLUSION ----
    full_response = str(r.headers) + r.text
    if MATCHER.lower() in full_response.lower():
        return

    print(f"[+] VALID ({r.status_code}) -> {url}")
    with open("result.txt", "a") as f:
        f.write(f"{r.status_code} {url}\n")

def wordlistReaderAndRequestCaller(base_url):
    path = "wordlist.txt" if WORDLIST.lower() == 'd' else WORDLIST
    with open(path, "r") as f:
        for line in f:
            payload = line.strip()
            if payload:
                requestSender(base_url + payload)

# ---------------- INPUT ----------------

RATE_LIMIT = int(input("Enter rate limit (requests per second): "))

raw_cookies = input("Paste cookies (key=value; key2=value2): ")
COOKIES = dict(item.split("=", 1) for item in raw_cookies.split(";") if "=" in item)

if input("Did you put headers in file? (Y/N): ").lower() == 'n':
    print("Paste headers (Ctrl+D | Ctrl+Z + Enter):")
    with open("headers.txt", "w") as f:
        f.write(sys.stdin.read())

HEADERS = load_headers()

MATCHER = input("Enter response text you DO NOT want to match: ")
WORDLIST = input("Enter wordlist path or D for default: ")
STATUS_CODE = input("Enter HTTP status code to match: ")

mode = input("Single endpoint or list? (S/L): ").lower()
askPermission()

if mode == 's':
    wordlistReaderAndRequestCaller(input("Paste endpoint: "))
else:
    with open(input("Path to URL list: "), "r") as f:
        for url in f:
            clean = url.strip()
            if clean:
                wordlistReaderAndRequestCaller(clean)

print(f"\nDone. Total requests sent: {TOTAL_REQUESTS}")
