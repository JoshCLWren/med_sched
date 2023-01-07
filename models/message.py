"""Message Model."""

from dataclasses import dataclass

from twilio.rest import Client


def authenticate_twilio():
    """Authenticate with twilio."""
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    return Client(account_sid, auth_token)


@dataclass
class Message:

    body: str
    to: str = os.environ["TWILIO_NUMBER"]
    from_: str = os.environ["TWILIO_NUMBER"]
    twilio_client = authenticate_twilio()

    def send(self):
        """Send a message."""
        self.twilio_client.messages.create(body=self.body, to=self.to, from_=self.from_)
