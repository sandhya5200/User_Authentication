from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
twilio_phone_number = os.getenv("twilio_phone_number")
client = Client(account_sid, auth_token)

def send_sms(to_number: str, body: str):
    return client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to=to_number
    )
