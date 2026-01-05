# THE DECEPTOR 😈

**My first real script**

A simple request-based testing/fuzzing script that sends crafted requests using custom headers, cookies, rate limiting, and wordlists.

Use responsibly.

---

## ⚙️ Usage

### 🍪 Cookies format

Cookies **must** be pasted as a single line, semicolon‑separated, exactly like a browser `Cookie` header:

__Host-session=abc123xyz456; _ga=GA1.2.123456789.1700000000; _gid=GA1.2.987654321.1700000000


- Do **not** paste cookies line-by-line  
- Do **not** include `Cookie:` at the start  

---

### 📌 Headers format

Headers must be pasted **one per line**, in raw HTTP header format.

You can either:
- paste them directly in the terminal when prompted, **or**
- place them in `headers.txt`

Correct example:

User-Agent: Mozilla/5.0
Accept: /
Authorization: Bearer abc


❌ Do **NOT** paste JSON  
❌ Do **NOT** include cookies in headers  
❌ Do **NOT** use `=` instead of `:`  

---

### 🌐 URLs & Endpoints

#### Single endpoint
Paste the **full URL**:

https://example.com/api/test


#### List of URLs
Each URL in the file **must include** the protocol:

http:// or https://


Examples:

https://example.com

http://test.site/api


Relative paths will **not** work.

---

### 📄 Wordlist

- Press `D` to use the default `wordlist.txt`
- Or provide a full path to a custom wordlist

Empty lines in wordlists are ignored.

---

### 🚦 Rate Limiting

You will be asked for a rate limit in **requests per second**.  
This is enforced internally to avoid accidental flooding.

---

## ⚠️ Disclaimer

This script is provided **as-is**.

You are fully responsible for how you use it.

I am **not responsible** for:
- system damage
- account bans
- rate limiting
- legal issues
- broken setups caused by misuse

If it breaks, you get to keep both pieces.

---

## 🧠 Notes

- Cookies and headers are handled separately — don’t mix them
- Silent failures usually mean malformed headers or cookies
- Read prompts carefully before pasting input
