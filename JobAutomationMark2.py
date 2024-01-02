import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time

# Twilio configuration
account_sid = 'Twilio Account SID'
auth_token = 'Twilio Auth Token'
from_number = '15055886138'
to_number = '15052280173'

# Scraping configuration
url = "https://www.linkedin.com/jobs/"
target_job_title = "Jr Python Developer"
previous_job_listings = set()

def send_sms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=message, from_=from_number, to=to_number)

def scrape_jobs():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return [listing.text for listing in soup.find_all('a', class_='job-listing')]
    return []

def main():
    while True:
        job_listings = scrape_jobs()

        new_job_listings = [job for job in job_listings if target_job_title in job and job not in previous_job_listings]

        if new_job_listings:
            sms_message = f"New {target_job_title} job alert:\n{'\n'.join(new_job_listings)}"
            send_sms(sms_message)
            previous_job_listings.update(new_job_listings)

        time.sleep(86400)  # 86400 seconds = 24 hours

if __name__ == "__main__":
    main()