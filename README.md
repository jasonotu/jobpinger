# JobPinger

## Description
JobPinger is a Python application that searches for job listings from various employers based on specified keywords. When new job listings are found, it can send email via Amazon SES to a predefined address.

## Features
- Scrapes job listings from multiple platforms including JazzHR, Lever, Workday, Njoyn, SuccessFactors, RSS feeds, or something custom as you define it.
- Supports keyword filtering to find relevant job postings.
- Provides verbose output for debugging.

## Requirements
- Python 3.x
- Packages as per requirements.txt
- Chrome driver if scraping from Workday or SuccessFactors
  
## Installation
Clone the repository:
   ```bash
   git clone https://github.com/jasonotu/jobpinger.git
   cd https://github.com/jasonotu/jobpinger.git
   ```

Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

Change config settings. Example:

```yaml
employers:
  Sophos:
    platform: lever
    url: "https://jobs.lever.co/sophos"
  Crowdstrike:
    platform: workday
    url: "https://crowdstrike.wd5.myworkdayjobs.com/crowdstrikecareers"

keywords:
  - "devops"
  - "security"

receiver_email: 'receiver@example.com'
sender_email: 'sender@example.com'
```

Run it! You could set it up as a cron job, make it a lambda function, etc.
   
```bash
~$ python main.py -v
Searching Sophos (lever)
Searching Crowdstrike (workday)
Found jobs!

Team Lead, MDR-Information Security Engineer at Sophos: https://jobs.lever.co/sophos/957dd87e-9923-4ca4-ae39-47909a28789a

Sr. Engineer, Application Security / Sensor - Product Security (Remote) at Crowdstrike: https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers/job/USA---Remote/Sr-Engineer--Application-Security---Sensor---Product-Security--Remote-_R20865

Sending pings!
```

### Options

- `-v`, `--verbose`: Show details on what is currently being scraped
- `-n`, `--no-email`: Skip sending email notifications.