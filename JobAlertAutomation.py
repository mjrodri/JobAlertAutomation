import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time

# Your Twilio Account SID and Authentication Token
account_sid = 'Twilio Account SID'
auth_token = 'Twilio Auth Token'

# Your Twilio phone number and recipient's phone number
from_number = '15055886138'
to_number: str = "15052280173"

# Website URL to scrape
url = "https://www.linkedin.com/jobs/"

# Specific job title to look for
target_job_title = "Jr Python Developer"

# Previous job listings (to identify new listings)
previous_job_listings = set()


def send_sms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )


while True:
    # Send an HTTP request to the job website
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract job listings
        job_listings = [listing.text for listing in soup.find_all('a', class_='job-listing')]

        # Find new job listings
        new_job_listings = [job for job in job_listings if target_job_title in job and job not in previous_job_listings]

        if new_job_listings:
            # Send SMS alerts for new job listings
            sms_message = "New {} job alert: \n{}".format(target_job_title, "\n".join(new_job_listings))
            send_sms(sms_message)

            # Update the previous job listings
            previous_job_listings.update(new_job_listings)

    # Add a delay before the next check (e.g., every 24 hours)
    time.sleep(86400)  # 86400 seconds = 24 hours
