"""Model of a prescription."""
import os
import random
from dataclasses import dataclass

from models.message import Message
from models.time import TimeOfDay


@dataclass
class Prescription:
    """Model of a prescription."""

    name: str = ""
    dosage: str = ""
    notes: str = ""
    morning_tablets = int = 0
    afternoon_tablets = int = 0
    evening_tablets = int = 0
    refills: int = 0
    refill_expiration_date: str = ""
    rx_number: int = 0
    owner_id: int = 0
    id: int = random.Random(10000)
    current_inventory: int = 0

    def refill(self):
        """Refill the prescription."""
        self.current_inventory += self.quantity

    def take(self):
        """Take a dose of the medication."""
        self.current_inventory -= self.tablets_per_dose

    def calculate_days_left(self):
        """Calculate the number of days left in the prescription."""
        return self.current_inventory / self.tablets_per_dose

    def send_refill_text(self, pharmacy):
        """Send a reminder to refill the prescription via twilio."""

        message = Message(
            body=f"You have {self.calculate_days_left()} days left of {self.brand}. Please refill your prescription. By calling {pharmacy.phone_number} or by going to {pharmacy.website}",
            to=os.environ["PHONE_NUMBER"],
        )
        message.send()
