# Amazon Job Watcher

_Automated job posting tracker for Amazon (or any site), with instant Discord notifications._

---

## Overview

I built this project because I kept missing job postings for my local Amazon fulfillment center. They were often gone within **30–45 minutes**, while existing online trackers only updated every 3–6 hours (unless you paid).  

This watcher monitors the job listings page in real time and immediately sends a notification to Discord whenever the page changes. Thanks to this, I got notified of an opening instantly and landed a job within a few days.  

Ironically, I realized I enjoyed **building the tracker far more than working at Amazon**—and it made me see how similar tooling could be expanded to track **any website changes** (not just job postings).  

---

## Features

- Uses **Playwright** to interact with dynamic job listing pages  
- Monitors for **page changes** using hashing  
- Sends **Discord webhook notifications** (instant push to phone/desktop)  
- Configurable for any URL or region  
- Runs via **GitHub Actions workflows**, locally, or on a server  

---

## Example Notification

Here’s how the Discord notification looks in action:

![Discord notification example](docs/discord-example.jpeg)

---

## Tech Stack

- [Playwright](https://playwright.dev/) – for reliable browser automation  
- [Requests](https://docs.python-requests.org/) – lightweight HTTP requests  
- [hashlib](https://docs.python.org/3/library/hashlib.html) – hashing to detect content changes  
- [mimetext](https://pypi.org/project/mimetext/) – email/message formatting  
- GitHub Actions – automated scheduled runs  

---

## Getting Started

### Prerequisites
- Python 3.8+  
- A Discord webhook URL (for notifications)  

### Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/Meritocaracies/amazon-job-watcher.git
cd amazon-job-watcher
pip install -r requirements.txt
