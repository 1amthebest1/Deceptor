import subprocess
import sys
import time

#---------------------------------------------------
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

# ---------------- GLOBAL VARIABLES ----------------

TOTAL_REQUESTS = 0
RATE_LIMIT = 0          # requests per second
RATE_LIMITER = 0

# ---------------- FUNCTIONS FIRST ----------------

def askPermission():
    permission = input("Do you want to start?, enter Y or N: ")
    if permission in ('y', 'Y'):
        return True
    else:
        sys.exit(0)


def requestSender(url):
    command = f'curl -b "{cookies}" -H @headers.txt "{url}" -i'
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    response = result.stdout
    first_line = response.split('\n', 1)[0]
    
    if matcher.lower() not in response.lower():
        if statusCode in first_line:
            print(f"potential valid request found {url}")
            with open('result.txt', 'a') as outfile:
                outfile.write(f"valid request found {url}\n")
        
    global TOTAL_REQUESTS, RATE_LIMITER

    TOTAL_REQUESTS += 1
    RATE_LIMITER += 1

    # ---- RATE LIMIT ----
    if RATE_LIMITER == RATE_LIMIT:
        time.sleep(1)
        RATE_LIMITER = 0
    # -------------------


def wordlistReaderAndRequestCaller(myUrl):
    if wordlist in ('d', 'D'):
        with open('wordlist.txt', 'r') as file:
            lines = file.readlines()
    else:
        with open(wordlist, 'r') as file:
            lines = file.readlines()

    for line in lines:
        payload = line.strip()
        if not payload:
            continue
        requestSender(myUrl + payload)

# ---------------- TAKE RATE LIMIT ----------------

RATE_LIMIT = int(input("Enter rate limit (requests per second): "))

# ---------------- READ HEADERS AND COOKIES ----------------

cookies = input("Please paste your cookies: ")

pastedInFile = input("Did you put the headers (Y/N): ")

if pastedInFile in ('N', 'n'):
    print("Paste headers (end with Ctrl+D on Linux/macOS or Ctrl+Z then Enter on Windows):")
    headers = sys.stdin.read()

    with open('headers.txt', 'w') as file:
        file.write(headers)

# ---------------- TAKES MATCHER, WORDLIST, AND ENDPOINT ----------------

matcher = input("Enter the response header text you do not want to match: ")
wordlist = input("Enter path for wordlist, or enter D for default: ")
statusCode = input("Enter the status code you want to match: ")

listOrSingle = input("Do you have a single endpoint or a list of URLs? (S/L): ")

if listOrSingle in ('s', 'S'):
    endpoint = input("Paste your endpoint: ")
    if askPermission():
        wordlistReaderAndRequestCaller(endpoint)

else:
    urlFilePath = input("Enter path containing list of URLs: ")
    if askPermission():
        with open(urlFilePath, 'r') as urlReader:
            urls = urlReader.readlines()
            for url in urls:
                clean_url = url.strip()
                if not clean_url:
                    continue
                wordlistReaderAndRequestCaller(clean_url)
