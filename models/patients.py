"""Model for a patient."""

from dataclasses import dataclass

import arrow

import db
from models.time import TimeOfDay


@dataclass
class Patient:
    """Model for a patient."""

    first_name: str = ""
    last_name: str = ""
    birth_date: str = ""
    id: int = None

    def __post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"
        self.age = self.calculate_age() if self.birth_date else None

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

    def save(self):
        """Save the patient."""
        # save a patient to the database
        try:
            self.id = db.insert(
                "patients",
                first_name=self.first_name,
                last_name=self.last_name,
                birth_date=self.birth_date,
            )
            return True
        except Exception as e:
            print(e)
            print("There was an error saving the patient.")
            return False

    def update(self):
        """Update the patient."""
        # update a patient in the database
        try:
            db.update(
                "patients",
                id=self.id,
                first_name=self.first_name,
                last_name=self.last_name,
                birth_date=self.birth_date,
            )
            return True
        except Exception as e:
            print(e)
            print("There was an error updating the patient.")
            return False

    def delete(self):

        try:
            return db.delete("patients", self.id)
        except Exception as e:
            print(e)
            print("There was an error deleting the patient.")
            return False

    def get_prescriptions(self):
        """Get the prescriptions for the patient."""
        return db.get_prescriptions_for_patient(self.id)

    def get_schedule(self):
        """Get the schedule for the patient."""
        return db.get_schedule_for_patient(self.id)

    def get_pharmacy(self):
        """Get the pharmacy for the patient."""
        return db.get_pharmacy_for_patient(self.id)

    def get(self, id):
        """Get the patient by id."""
        patient = db.get("patients", id)
        self.id = patient[0]
        self.first_name = patient[1]
        self.last_name = patient[2]
        self.birth_date = patient[3]
        return self
