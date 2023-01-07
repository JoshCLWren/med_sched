"""Model of a prescription."""
import os
from dataclasses import dataclass

from models.message import Message
from models.time import TimeOfDay


@dataclass
class Prescription:
    """Model of a prescription."""

    dosage: str
    frequency: str
    generic: str
    brand: str
    notes: str
    is_generic: bool
    time_of_day: TimeOfDay
    instructions: str
    quantity: int
    refills: int
    refill_expiration_date: str
    rx_number: int
    owner_id: int
    created_at: str
    updated_at: str
    id: int
    current_inventory: int
    tablets_per_dose = int

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
