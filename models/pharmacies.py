"""Model for a pharmacy."""

import random
from dataclasses import dataclass

import db
from models.time import TimeOfDay


@dataclass
class Pharmacy:
    """Model for a pharmacy."""

    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    fax_number: str
    email: str
    website: str
    is_default: bool
    created_at: str
    updated_at: str
    id: int = random.randint(10000, 99999)

    def save(self):
        """Save the pharmacy."""
        try:
            self.id = db.insert(
                "pharmacies",
                **self.__dict__,
            )
            return True
        except Exception as e:
            print(e)
            print("There was an error saving the pharmacy.")
            return False
