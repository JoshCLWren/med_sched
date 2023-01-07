"""Model for a patient."""

from dataclasses import dataclass

import arrow

from models.time import TimeOfDay


@dataclass
class Patient:
    """Model for a patient."""

    first_name: str
    last_name: str
    birth_date: str

    def __post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"
        self.age = self.calculate_age()

    def calculate_age(self):
        """Calculate the age of the patient."""
        current_date = arrow.utcnow()
        birth_date = arrow.get(self.birth_date)
        return (
            current_date.year
            - birth_date.year
            - (
                (current_date.month, current_date.day)
                < (birth_date.month, birth_date.day)
            )
        )
