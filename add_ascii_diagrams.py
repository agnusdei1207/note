import os
import glob
import re

diagrams = {
    "admin": """
```text
[ Attacker ] --(Cookie: role=admin)--> [ Web Server ]
                                       |-- Check req.cookies.role
                                       |-- Grant Admin Access!
```
""",
    "ato": """
```text
[ Attacker ] --(Change password for target user)--> [ Web Server ]
                                                    |-- Missing Authorization Check
                                                    |-- Password Changed!
```
""",
    "brute": """
```text
[ Attacker ] --(Brute Force / FFuF)--> [ Web Server ]
             |-- Pwd1                  |-- Invalid
             |-- Pwd2                  |-- Invalid
             |-- ...                   |-- ...
             |-- CorrectPwd            |-- Access Granted!
```
""",
    "cache": """
```text
[ Attacker ] --(Malicious Header/Payload)--> [ Cache Server (Varnish) ] --> [ Web Server ]
                                             |-- Caches Malicious Response
[ Victim ]   --(Normal Request)------------> [ Cache Server ]
                                             |-- Returns Poisoned Cache!
```
""",
    "clickjack": """
```text
[ Victim's Browser ]
|---------------------------------|
| [ Attacker's Fake UI (Z-index:2]|
| "CLICK HERE FOR FREE PRIZE"     |
|                                 |
| [ Target UI (Z-index:1, Opac:0)]|
| "DELETE ACCOUNT BUTTON"         |
|---------------------------------|
```
""",
    "cmdi": """
```text
[ Attacker ] --(Input: 8.8.8.8 ; id)--> [ Web Server ]
                                        |-- OS Command Execution
                                        |-- Runs: ping 8.8.8.8 ; id
                                        |-- Returns Output
```
""",
    "container": """
```text
[ Container (Web Shell) ]
|-- /var/run/docker.sock (Mounted)
|-- [ Docker CLI ] --(Deploy Privileged Container)--> [ Host OS ]
                                                      |-- Root Compromised!
```
""",
    "cors": """
```text
[ Victim's Browser ]
|-- Visits Attacker.com
|-- AJAX Request to Target.com --(with Cookies)--> [ Target.com API ]
                                                   |-- Allows * Origin
<-- Sensitive Data Returned -----------------------|
|-- Exfiltrates Data to Attacker
```
""",
    "crlf": """
```text
[ Attacker ] --(Input: %0d%0a%0d%0a<script>...)--> [ Web Server ]
                                                   |-- Injects CRLF in Headers
                                                   |-- Splits HTTP Response
<-- [ HTTP Headers ] \r\n\r\n [ Malicious Body ] --|
```
""",
    "crypto": """
```text
[ Attacker ]
|-- Intercepts Ciphertext/Token
|-- Analyzes Pattern (ECB Block, Base64, etc.)
|-- Cuts/Pastes/Decodes/Spoofs
|-- Sends Forged Token --> [ Web Server ]
                           |-- Accepts Forged Token
```
""",
    "csrf": """
```text
[ Victim (Logged In) ]
|-- Visits Attacker Site
|-- Auto-submits Hidden Form --(Valid Cookie)--> [ Web Server ]
                                                 |-- Missing CSRF Token
                                                 |-- Executes Action (e.g. Email Change)
```
""",
    "deser": """
```text
[ Attacker ] --(Serialized Malicious Object)--> [ Web Server ]
                                                |-- unserialize()
                                                |-- Magic Methods (__destruct) Triggered
                                                |-- RCE / File Write
```
""",
    "header-inject": """
```text
[ Attacker ] --(Host: attacker.com)--> [ Web Server ]
                                       |-- Generates Password Reset Link
<-- Link: http://attacker.com/reset ---|
```
""",
    "host": """
```text
[ Attacker ] --(Host: attacker.com)--> [ Web Server ]
                                       |-- Generates Password Reset Link
<-- Link: http://attacker.com/reset ---|
```
""",
    "idor": """
```text
[ Attacker (ID: 1) ] --(GET /profile?id=2)--> [ Web Server ]
                                              |-- Missing Ownership Check
                                              |-- Returns User 2's Profile
```
""",
    "info-disc": """
```text
[ Attacker ] --(Directory Brute Force)--> [ Web Server ]
                                          |-- /config.php.bak
                                          |-- /.git/
                                          |-- Returns Sensitive Files
```
""",
    "jwt": """
```text
[ Attacker ]
|-- Decodes JWT
|-- Modifies Payload (role: admin)
|-- Signs with 'None' alg / Cracked Secret --> [ Web Server ]
                                               |-- Trusts JWT
```
""",
    "ldap": """
```text
[ Attacker ] --(Input: admin)(password=A*)--> [ LDAP Server ]
                                              |-- Evaluates Filter
                                              |-- True/False Response
```
""",
    "lfi": """
```text
[ Attacker ] --(file=../../../../etc/passwd)--> [ Web Server ]
                                                |-- include(../../../../etc/passwd)
<-- Contents of /etc/passwd --------------------|
```
""",
    "log-inject": """
```text
[ Attacker ] --(Input: test\\n[SUCCESS] Admin logged in)--> [ Web Server ]
                                                            |-- Writes to Log
[ Log File ]
|-- INFO - test
|-- [SUCCESS] Admin logged in
```
""",
    "logic": """
```text
[ Attacker ] --(Buy -10 Items)--> [ Web Server ]
                                  |-- Total = -500
                                  |-- Balance = Balance - (-500)
                                  |-- Balance Increased!
```
""",
    "mfa": """
```text
[ Attacker ] --(mfa_required=false)--> [ Web Server ]
                                       |-- Trusts Client Parameter
                                       |-- Bypasses MFA
```
""",
    "multistage": """
```text
[ XSS ] --(Steal Cookie)--> [ IDOR ] --(Find Admin Panel)--> [ File Upload ] --(Web Shell)--> [ RCE ]
```
""",
    "nosqli": """
```text
[ Attacker ] --({"username":{"$ne":null}, "password":{"$ne":null}})--> [ NoSQL DB ]
                                                                       |-- Condition is True
                                                                       |-- Returns Admin Record
```
""",
    "oauth": """
```text
[ Attacker ] --(redirect_uri=attacker.com)--> [ OAuth Server ]
                                              |-- Redirects Victim with Auth Code
[ Victim ]   --(Sends Auth Code)------------> [ Attacker Server ]
```
""",
    "pass-reset": """
```text
[ Attacker ] --(Target: admin@luxora, Host: attacker.com)--> [ Web Server ]
                                                             |-- Sends email to Admin
[ Admin ]    --(Clicks Link)-------------------------------> [ Attacker Server ]
                                                             |-- Token Stolen!
```
""",
    "payment": """
```text
[ Attacker ] --(Price: $1)--> [ Web Server ]
                              |-- Trusts Client Price
                              |-- Deducts $1
                              |-- Item Purchased!
```
""",
    "persist": """
```text
[ Web Shell ] --(Write to ~/.ssh/authorized_keys)--> [ Host OS ]
[ Attacker ]  --(SSH Login with Private Key)-------> [ Host OS ]
                                                     |-- Permanent Access!
```
""",
    "postmsg": """
```text
[ Attacker Site ] --(postMessage(Malicious Data))--> [ Target iframe ]
                                                     |-- Missing Origin Check
                                                     |-- Executes DOM XSS
```
""",
    "privesc": """
```text
[ Low Priv User ] --(Run SUID Binary / PATH Injection)--> [ Root Shell ]
```
""",
    "proto": """
```text
[ Attacker ] --({"__proto__": {"role": "admin"}})--> [ Web Server ]
                                                     |-- merge()
                                                     |-- Global Object Polluted
```
""",
    "race": """
```text
[ Attacker ] --(Thread 1: Use Coupon)--> [ Web Server ] --(Check DB)--> Valid
[ Attacker ] --(Thread 2: Use Coupon)--> [ Web Server ] --(Check DB)--> Valid
                                         |-- Both Apply Discount!
```
""",
    "ratelimit": """
```text
[ Attacker ] --(IP 1)--> [ Server ]
[ Attacker ] --(IP 2)--> [ Server ]
[ Attacker ] --(IP 3)--> [ Server ]
                         |-- Rate Limit Bypassed by IP Rotation
```
""",
    "rbac": """
```text
[ Normal User ] --(GET /api/admin/users)--> [ Web Server ]
                                            |-- Missing Role Check
                                            |-- Returns Admin Data
```
""",
    "redirect": """
```text
[ Victim ] --(GET /login?next=//attacker.com)--> [ Web Server ]
                                                 |-- Redirects to Attacker Site
```
""",
    "reverse": """
```text
[ Binary ] --(Hex Edit: JZ -> NOP)--> [ Patched Binary ]
                                      |-- Always Validates License
```
""",
    "rfi": """
```text
[ Attacker ] --(url=http://attacker.com/shell.txt)--> [ Web Server ]
                                                      |-- Downloads & Executes Code
```
""",
    "secret": """
```text
[ Attacker ] --(View Source)--> [ JS File / .map File ]
                                |-- API_KEY = "XYZ123"
                                |-- Extracted!
```
""",
    "session": """
```text
[ Attacker ] --(Inject Session ID)--> [ Victim's Browser ]
[ Victim ]   --(Logs In)------------> [ Web Server ]
[ Attacker ] --(Uses Same Session)-> [ Web Server ]
                                     |-- Logged in as Victim!
```
""",
    "smuggle": """
```text
[ Attacker ] --(CL.TE Malformed Request)--> [ Front-end Proxy (Reads CL) ]
                                            |-- Forwards as One Request
                                            [ Back-end Server (Reads TE) ]
                                            |-- Splits into Two Requests!
```
""",
    "sqli": """
```text
[ Attacker ] --(Input: ' OR 1=1 -- )--> [ Web Server ]
                                        |-- Query: SELECT * FROM users WHERE name='' OR 1=1 --'
                                        |-- Returns All Users
```
""",
    "ssrf": """
```text
[ Attacker ] --(url=http://169.254.169.254)--> [ Web Server ]
                                               |-- Fetches Metadata
<-- Metadata Returned -------------------------|
```
""",
    "ssti": """
```text
[ Attacker ] --(Input: {{7*7}})--> [ Web Server ]
                                   |-- Template Engine Evaluates
<-- Returns: 49 -------------------|
```
""",
    "timing": """
```text
[ Attacker ] --(Guess: A)--> [ Server ] (Returns in 10ms)
[ Attacker ] --(Guess: B)--> [ Server ] (Returns in 10ms)
[ Attacker ] --(Guess: C)--> [ Server ] (Returns in 50ms) -> Correct Char!
```
""",
    "upload": """
```text
[ Attacker ] --(Upload shell.php.jpg)--> [ Web Server ]
                                         |-- Saved to /uploads/
[ Attacker ] --(GET /uploads/shell.php)--> [ Web Server ]
                                           |-- Executes PHP Code!
```
""",
    "webshell": """
```text
[ Attacker ] --(GET shell.php?cmd=ls)--> [ Web Server ]
                                         |-- system('ls')
<-- Directory Listing -------------------|
```
""",
    "xpath": """
```text
[ Attacker ] --(Input: ' or '1'='1)--> [ Web Server ]
                                       |-- XPath Query Evaluated
<-- XML Data Returned -----------------|
```
""",
    "xss": """
```text
[ Attacker ] --(Injects <script>)--> [ Web Server / Browser ]
                                     |-- Script Executed
                                     |-- Steals Cookies / Actions
```
""",
    "xxe": """
```text
[ Attacker ] --(XML with <!ENTITY xxe SYSTEM "file:///etc/passwd">)--> [ Web Server ]
                                                                       |-- Parses XML & Reads File
<-- File Contents Returned --------------------------------------------|
```
"""
}

# Function to inject diagram
def inject_diagram(file_path, category):
    diagram = diagrams.get(category)
    if not diagram:
        print(f"No diagram found for {category}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid injecting multiple times
    if "```text\n[" in content and "-->" in content:
        print(f"Already injected in {file_path}")
        return

    # Try to inject after "## 💥 2. 취약점 식별" or similar section
    # Alternatively, inject after "---" following Reconnaissance
    
    inject_point_regex = r"(## 💥 2\.[^\n]+)"
    match = re.search(inject_point_regex, content)
    
    if match:
        injection = match.group(1) + "\n\n### 📊 공격 흐름도 (Attack Flow)\n" + diagram
        content = content.replace(match.group(1), injection, 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected into {file_path}")
    else:
        print(f"Could not find injection point in {file_path}")

base_dir = "content/study/vulnable_ctf"
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".md") and file != "_index.md":
            category = os.path.basename(root)
            file_path = os.path.join(root, file)
            inject_diagram(file_path, category)

print("Done inserting diagrams.")
