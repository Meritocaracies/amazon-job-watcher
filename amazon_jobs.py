import requests
import hashlib
import os
import argparse
import smtplib
from email.mime.text import MIMEText

# -----------------------------
# SETTINGS (use GitHub secrets)
# -----------------------------
URL = "https://hiring.amazon.com/app#/jobSearch?query=&postal=99004&locale=en-US"
CHECK_FILE = "last_page_hash.txt"

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")  # can be email or Google Voice
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")  # Discord webhook URL

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def fetch_page():
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.text

def compute_hash(content):
    return hashlib.md5(content.encode("utf-8")).hexdigest()

def load_last_hash():
    if os.path.exists(CHECK_FILE):
        with open(CHECK_FILE, "r") as f:
            return f.read().strip()
    return None

def save_hash(hash_value):
    with open(CHECK_FILE, "w") as f:
        f.write(hash_value)

def send_email_alert(message):
    msg = MIMEText(message)
    msg["Subject"] = "[Amazon Jobs Alert] Page changed"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def send_discord_alert(message):
    if not DISCORD_WEBHOOK:
        print("❌ Discord webhook not set.")
        return
    import requests
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK, json=data)
    if response.status_code == 204:
        print("✅ Discord alert sent")
    else:
        print("❌ Failed to send Discord alert:", response.text)

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main(test_mode=False):
    if test_mode:
        print("⚡ Test mode active – sending alert without checking page.")
        message = f"[TEST] Amazon jobs page alert: {URL}"
        send_email_alert(message)
        send_discord_alert(message)
        return

    page = fetch_page()
    current_hash = compute_hash(page)
    last_hash = load_last_hash()

    if last_hash != current_hash:
        print("✅ Page changed! Sending alerts.")
        message = f"Amazon jobs page has changed: {URL}"
        send_email_alert(message)
        send_discord_alert(message)
        save_hash(current_hash)
    else:
        print("No change detected.")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send a test alert")
    args = parser.parse_args()
    main(test_mode=args.test)
