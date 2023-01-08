"""Classes representing when medicine needs to be taken and refilled."""

import pickle
import random
from dataclasses import dataclass

import arrow

import db
from models.time import TimeOfDay


@dataclass
class Schedule:
    """A schedule for taking medicine for morning, afternoon, and evening."""

    morning_medication: list
    afternoon_medication: list
    evening_medication: list
    patient_id: int = None
    id: int = random.Random(10000)

    def get_morning_medication(self):
        """Get the morning medication."""
        return self.morning_medication

    def get_afternoon_medication(self):
        """Get the afternoon medication."""
        return self.afternoon_medication

    def get_evening_medication(self):
        """Get the evening medication."""
        return self.evening_medication

    def get_all_medication(self):
        """Get all medication."""
        return (
            self.morning_medication
            + self.afternoon_medication
            + self.evening_medication
        )

    def get_medication_by_time_of_day(self, time_of_day):

        if time_of_day == TimeOfDay.MORNING:
            return self.get_morning_medication()
        elif time_of_day == TimeOfDay.AFTERNOON:
            return self.get_afternoon_medication()
        elif time_of_day == TimeOfDay.EVENING:
            return self.get_evening_medication()
        else:
            return None

    def check_for_refills(self):
        """Check for refills."""
        for medication in self.get_all_medication():
            if medication.calculate_days_left() < 7:
                medication.send_refill_text()

    def save(self):
        """Save the schedule."""
        # pickle the medication lists
        pickled_morning_medication = pickle.dumps(self.morning_medication)
        pickled_afternoon_medication = pickle.dumps(self.afternoon_medication)
        picked_evening_medication = pickle.dumps(self.evening_medication)
        try:
            self.id = db.insert(
                "schedules",
                morning_medication=pickled_morning_medication,
                afternoon_medication=pickled_afternoon_medication,
                evening_medication=picked_evening_medication,
                patient_id=self.patient_id,
            )
            return True
        except Exception as e:
            print(e)
            print("There was an error saving the schedule.")
            return False

    def load(self, id):
        """Load the schedule."""
        schedule = db.get("schedules", id)
        # unpickle the medication lists
        self.morning_medication = pickle.loads(schedule["morning_medication"])
        self.afternoon_medication = pickle.loads(schedule["afternoon_medication"])
        self.evening_medication = pickle.loads(schedule["evening_medication"])
        self.patient_id = schedule["patient_id"]
        self.id = schedule["id"]
        return self.__dict__
