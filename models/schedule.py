"""Classes representing when medicine needs to be taken and refilled."""

from dataclasses import dataclass

import arrow

from models.time import TimeOfDay


@dataclass
class DailySchedule:
    """A schedule for taking medicine for morning, afternoon, and evening."""

    morning_medication: list
    afternoon_medication: list
    evening_medication: list

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
