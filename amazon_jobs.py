import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import json
import os
import sys

# SETTINGS
URL = "https://hiring.amazon.com/app#/jobSearch?query=&postal=99004&locale=en-US"
CHECK_FILE = "seen_jobs.json"
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def fetch_jobs():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = soup.select("div.job-tile")  # selector may change depending on page structure
    job_list = []
    for job in jobs:
        title = job.select_one("h3").get_text(strip=True)
        link = "https://www.amazon.jobs" + job.select_one("a")["href"]
        job_list.append({"title": title, "link": link})
    return job_list

def load_seen():
    if os.path.exists(CHECK_FILE):
        with open(CHECK_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen(jobs):
    with open(CHECK_FILE, "w") as f:
        json.dump(jobs, f)

def send_email(new_jobs):
    body = "\n".join([f"{j['title']}: {j['link']}" for j in new_jobs])
    msg = MIMEText(body)
    msg["Subject"] = f"[Amazon Jobs Alert] {len(new_jobs)} new job(s) posted"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def main(test_mode=False):
    if test_mode:
        new_jobs = [{"title": "TEST JOB", "link": "https://example.com"}]
        send_email(new_jobs)
        print("✅ Test email sent")
        return

    jobs = fetch_jobs()
    seen = load_seen()
    new_jobs = [j for j in jobs if j not in seen]

    if new_jobs:
        send_email(new_jobs)
        save_seen(jobs)
        print(f"✅ Sent {len(new_jobs)} new jobs")
    else:
        print("No new jobs found.")

if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    main(test_mode=test_mode)
