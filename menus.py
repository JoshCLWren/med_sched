from dataclasses import dataclass

import db
import models


@dataclass
class Menu:
    title = "Main Menu"
    options = ["Patients", "Prescriptions", "Schedule", "Pharmacies"]

    def display(self):
        print(self.title)
        for index, option in enumerate(self.options):
            print(f"{index + 1}. {option}")

    def get_user_input(self):
        try:
            while True:
                self.display()
                user_input = input("Select an option: ")
                try:
                    user_input = int(user_input)
                    if user_input in range(1, len(self.options) + 1):
                        print(f"You chose {self.options[user_input - 1]}")
                        choice = {1: PatientsMenu, 2: PrescriptionsMenu, 3: ScheduleMenu, 4: PharmaciesMenu}
                        self.choice_action(choice[user_input])
                    else:
                        print("Please enter a valid choice.")
                        continue
                except Exception:
                    if isinstance(user_input, str) and user_input.lower() in ["q", "quit", "exit", "x"]:
                        print("Goodbye!")
                        break
                    else:
                        print("Please enter a valid choice.")
                        continue

        except KeyboardInterrupt:
            print("Goodbye!")

    @staticmethod
    def choice_action(cls):
        sub_menu = cls()
        sub_menu.display()
        sub_menu.get_user_input()


@dataclass
class PatientsMenu(Menu):
    title = "Patients Menu"
    options = ["Add Patient", "View Patients", "Edit Patient", "Delete Patient", "Back"]

    def get_user_input(self):
        try:
            while True:
                choice = input("Enter a choice or x to exit: ")
                try:
                    print(f"You chose {self.options[int(choice) - 1]}")
                    choice = int(choice)
                    if choice == 1:
                        print("Let's add a patient!")
                        print("Enter the patient's first name: ")
                        first_name = input()
                        print("Enter the patient's last name: ")
                        last_name = input()
                        print("Enter the patient's birth date in YYYY/MM/DD format: ")
                        birth_date = arrow.get(input()).isoformat()
                        patient = models.patients.Patient(
                            first_name=first_name,
                            last_name=last_name,
                            birth_date=birth_date,
                        )
                        patient.save()
                        print("Patient saved!")
                        self.display()
                    elif choice == 2:
                        print("Here are all the patients:")
                        patients = db.get_all("patients")
                        for patient in patients:
                            print(patient)
                        self.display()
                    elif choice == 3:
                        print("Let's edit a patient!")
                        print("Enter the patient's id: ")
                        patient_id = int(input())
                        patient = models.patients.Patient(id=patient_id).get(patient_id)
                        print(
                            "Press enter after you are done editing the patient's first name or press enter to leave it this way."
                        )
                        print(f"Current first name: {patient.first_name}")
                        first_name = input() or patient.first_name
                        print(
                            "Press enter after you are done editing the patient's last name or press enter to leave it this way."
                        )
                        print(f"Current last name: {patient.last_name}")
                        last_name = input() or patient.last_name
                        print(
                            "Press enter after you are done editing the patient's birth date or press enter to leave it this way."
                        )
                        print(f"Current birth date: {patient.birth_date}")
                        birth_date = input() or patient.birth_date
                        patient.first_name = first_name
                        patient.last_name = last_name
                        patient.birth_date = birth_date
                        patient.update()
                        print("Patient updated!")
                        self.display()
                    elif choice == 4:
                        print(
                            "Let's delete a patient, it probably isn't working though..."
                        )
                        print("Enter the patient's id: ")
                        patient_id = input()
                        db.delete("patients", patient_id)
                        print("Patient deleted... maybe!")
                        self.display()
                    elif choice == 5:
                        break
                except ValueError:
                    if choice.lower() == "x":
                        print("Goodbye!")
                        break
                    print("Please enter a valid choice.")
                    continue
        except KeyboardInterrupt:
            print("Goodbye!")


@dataclass
class PrescriptionsMenu(Menu):
    title = "Prescriptions Menu"
    options = [
        "Add Prescription",
        "View Prescriptions",
        "Edit Prescription",
        "Delete Prescription",
        "Back",
    ]

    def get_user_input(self):
        """Get user input for the Prescription menu."""

        try:
            while True:
                choice = input("Enter a choice or x to exit: ")
                try:
                    print(f"You chose {self.options[int(choice) - 1]}")
                    choice = int(choice)
                    if choice == 1:
                        print("Let's add a prescription!")
                        prescription = models.prescriptions.Prescription()
                        print("Enter the prescription's name: ")
                        prescription.name = input()
                        print("Enter the mg of each tablet: ")
                        prescription.dosage = input()
                        print("Enter the prescription's notes: ")
                        prescription.patient_id = int(input())
                        print("Is this taken in the morning? (y/n)")
                        take_in_morning = input()
                        if take_in_morning == "y":
                            print("How many tablets are taken in the morning?")
                            prescription.morning_tablets = int(input())

                        else:
                            prescription.morning_tablets = 0
                        print("Is this taken in the afternoon? (y/n)")
                        take_in_afternoon = input()
                        if take_in_afternoon == "y":
                            print("How many tablets are taken in the afternoon?")
                            prescription.afternoon_tablets = int(input())

                        else:
                            prescription.afternoon_tablets = 0

                        print("Is this taken in the evening? (y/n)")
                        take_in_evening = input()
                        if take_in_evening == "y":
                            print("How many tablets are taken in the evening?")
                            prescription.evening_tablets = int(input())

                        else:
                            prescription.evening_tablets = 0
                        print("How many tablets are in the bottle currently?")
                        prescription.current_inventory = int(input())
                        print("How many refills are left?")
                        prescription.refills = int(input())
                        print("What is the prescription's rx number?")
                        prescription.rx_number = int(input())
                        print("Do the refills expire?")
                        refills_expire = input()
                        if refills_expire == "y":
                            print("When do the refills expire? (YYYY/MM/DD)")
                            prescription.refill_expiration_date = arrow.get(
                                input()
                            ).isoformat()
                        else:

                            prescription.refill_expiration_date = None
                        prescription.save()
                        print("Prescription saved!")
                        self.display()
                    elif choice == 2:

                        print("Here are all the prescriptions:")
                        prescriptions = db.get_all("prescriptions")
                        for prescription in prescriptions:

                            print(prescription)
                        self.display()
                    elif choice == 3:
                        print("Let's edit a prescription!")
                        print("Enter the prescription's id: ")
                        prescription_id = int(input())
                        prescription = models.prescriptions.Prescription(
                            id=prescription_id
                        ).get(prescription_id)
                        print(
                            "Press enter after you are done editing the prescription's name or press enter to leave it this way."
                        )
                        print(f"Current name: {prescription.name}")
                        name = input() or prescription.name
                        print(
                            "Press enter after you are done editing the prescription's dosage or press enter to leave it this way."
                        )
                        print(f"Current dosage: {prescription.dosage}")
                        dosage = input() or prescription.dosage
                        print(
                            "Press enter after you are done editing the prescription's notes or press enter to leave it this way."
                        )
                        print(f"Current notes: {prescription.notes}")
                        notes = input() or prescription.notes
                        print(
                            "Press enter after you are done editing the prescription's patient id or press enter to leave it this way."
                        )
                        print(f"Current patient id: {prescription.patient_id}")
                        patient_id = input() or prescription.patient_id
                        print(
                            "Press enter after you are done editing the prescription's morning tablets or press enter to leave it this way."
                        )
                        print(
                            f"Current morning tablets: {prescription.morning_tablets}"
                        )
                        morning_tablets = input() or prescription.morning_tablets
                        print(
                            "Press enter after you are done editing the prescription's afternoon tablets or press enter to leave it this way."
                        )
                        print(
                            f"Current afternoon tablets: {prescription.afternoon_tablets}"
                        )
                        afternoon_tablets = input() or prescription.afternoon_tablets
                        print(
                            "Press enter after you are done editing the prescription's evening tablets or press enter to leave it this way."
                        )
                        print(
                            f"Current evening tablets: {prescription.evening_tablets}"
                        )
                        evening_tablets = input() or prescription.evening_tablets
                        print(
                            "Press enter after you are done editing the prescription's current inventory or press enter to leave it this way."
                        )
                        print(
                            f"Current current inventory: {prescription.current_inventory}"
                        )
                        current_inventory = input() or prescription.current_inventory
                        print(
                            "Press enter after you are done editing the prescription's refills or press enter to leave it this way."
                        )
                        print(f"Current refills: {prescription.refills}")
                        refills = input() or prescription.refills
                        print(
                            "Press enter after you are done editing the prescription's rx number or press enter to leave it this way."
                        )
                        print(f"Current rx number: {prescription.rx_number}")
                        rx_number = input() or prescription.rx_number
                        print(
                            "Press enter after you are done editing the prescription's refill expiration date or press enter to leave it this way."
                        )
                        print(
                            f"Current refill expiration date: {prescription.refill_expiration_date}"
                        )
                        refill_expiration_date = (
                            input() or prescription.refill_expiration_date
                        )
                        prescription.name = name
                        prescription.dosage = dosage
                        prescription.notes = notes
                        prescription.patient_id = patient_id
                        prescription.morning_tablets = morning_tablets
                        prescription.afternoon_tablets = afternoon_tablets
                        prescription.evening_tablets = evening_tablets
                        prescription.current_inventory = current_inventory
                        prescription.refills = refills
                        prescription.rx_number = rx_number
                        prescription.refill_expiration_date = refill_expiration_date
                        prescription.save()
                        print("Prescription saved!")
                        self.display()
                    elif choice == 4:
                        print("Let's delete a prescription!")
                        print("Enter the prescription's id: ")
                        prescription_id = int(input())
                        prescription = models.prescriptions.Prescription(
                            id=prescription_id
                        ).get(prescription_id)
                        prescription.delete()
                        print("Prescription deleted!")
                        self.display()
                    elif choice == 5:
                        break
                    else:
                        print("That's not a valid choice!")
                        self.display()
                except ValueError:
                    print("That's not a valid choice!")
                    self.display()
        except KeyboardInterrupt:
            print("Goodbye!")
            exit()


@dataclass
class ScheduleMenu(Menu):
    title = "Schedule Menu"
    options = [
        "Add Schedule",
        "View Schedule",
        "Edit Schedule",
        "Delete Schedule",
        "Back",
    ]

    def get_user_input(self):

        try:
            while True:
                try:
                    choice = int(input())
                    if choice == 1:
                        print("Let's add a schedule!")
                        schedule = models.schedules.Schedule()
                        print("What is the schedule's name?")
                        schedule.name = input()
                        print("What is the schedule's notes?")
                        schedule.notes = input()
                        print("What is the schedule's patient id?")
                        schedule.patient_id = int(input())
                        print("What is the schedule's prescription id?")
                        schedule.prescription_id = int(input())
                        print("What is the schedule's start date? (YYYY/MM/DD)")
                        schedule.start_date = arrow.get(input()).isoformat()
                        print("What is the schedule's end date? (YYYY/MM/DD)")
                        schedule.end_date = arrow.get(input()).isoformat()
                        schedule.save()
                        print("Schedule saved!")
                        self.display()
                    elif choice == 2:
                        print("Here are all the schedules:")
                        schedules = db.get_all("schedules")
                        for schedule in schedules:

                            print(schedule)
                        self.display()
                    elif choice == 3:
                        print("Let's edit a schedule!")
                        print("Enter the schedule's id: ")
                        schedule_id = int(input())
                        schedule = models.schedules.Schedule(id=schedule_id).get(
                            schedule_id
                        )
                        print(
                            "Press enter after you are done editing the schedule's name or press enter to leave it this way."
                        )
                        print(f"Current name: {schedule.name}")
                        name = input() or schedule.name
                        print(
                            "Press enter after you are done editing the schedule's notes or press enter to leave it this way."
                        )
                        print(f"Current notes: {schedule.notes}")
                        notes = input() or schedule.notes

                        print(
                            "Press enter after you are done editing the schedule's patient id or press enter to leave it this way."
                        )
                        print(f"Current patient id: {schedule.patient_id}")
                        patient_id = input() or schedule.patient_id
                        print(
                            "Press enter after you are done editing the schedule's prescription id or press enter to leave it this way."
                        )
                        print(f"Current prescription id: {schedule.prescription_id}")
                        prescription_id = input() or schedule.prescription_id
                        print(
                            "Press enter after you are done editing the schedule's start date or press enter to leave it this way."
                        )
                        print(f"Current start date: {schedule.start_date}")
                        start_date = input() or schedule.start_date
                        print(
                            "Press enter after you are done editing the schedule's end date or press enter to leave it this way."
                        )
                        print(f"Current end date: {schedule.end_date}")
                        end_date = input() or schedule.end_date
                        schedule.name = name
                        schedule.notes = notes
                        schedule.patient_id = patient_id
                        schedule.prescription_id = prescription_id
                        schedule.start_date = start_date
                        schedule.end_date = end_date
                        schedule.save()
                        print("Schedule saved!")
                        self.display()
                    elif choice == 4:
                        print("Let's delete a schedule!")
                        print("Enter the schedule's id: ")
                        schedule_id = int(input())
                        schedule = models.schedules.Schedule(id=schedule_id).get(
                            schedule_id
                        )
                        schedule.delete()
                        print("Schedule deleted!")
                        self.display()
                    elif choice == 5:
                        break
                    else:
                        print("That's not a valid choice!")
                        self.display()
                except ValueError:
                    print("That's not a valid choice!")
                    self.display()
        except KeyboardInterrupt:
            print("Goodbye!")
            exit()


@dataclass
class PharmaciesMenu(Menu):
    title = "Pharmacies Menu"
    options = [
        "Add Pharmacy",
        "View Pharmacies",
        "Edit Pharmacy",
        "Delete Pharmacy",
        "Back",
    ]

    def get_user_input(self):
        try:
            while True:
                try:
                    choice = int(input())
                    if choice == 1:
                        print("Let's add a pharmacy!")
                        pharmacy = models.pharmacies.Pharmacy()
                        print("What is the pharmacy's name?")
                        pharmacy.name = input()
                        print("What is the pharmacy's address?")
                        pharmacy.address = input()
                        print("What is the pharmacy's phone number?")
                        pharmacy.phone_number = input()
                        pharmacy.save()
                        print("Pharmacy saved!")
                        self.display()
                    elif choice == 2:
                        print("Here are all the pharmacies:")
                        pharmacies = db.get_all("pharmacies")
                        for pharmacy in pharmacies:
                            print(pharmacy)
                        self.display()
                    elif choice == 3:
                        print("Let's edit a pharmacy!")
                        print("Enter the pharmacy's id: ")
                        pharmacy_id = int(input())
                        pharmacy = models.pharmacies.Pharmacy(id=pharmacy_id).get(
                            pharmacy_id
                        )
                        print(
                            "Press enter after you are done editing the pharmacy's name or press enter to leave it this way."
                        )
                        print(f"Current name: {pharmacy.name}")
                        name = input() or pharmacy.name
                        print(
                            "Press enter after you are done editing the pharmacy's address or press enter to leave it this way."
                        )
                        print(f"Current address: {pharmacy.address}")
                        address = input() or pharmacy.address
                        print(
                            "Press enter after you are done editing the pharmacy's phone number or press enter to leave it this way."
                        )
                        print(f"Current phone number: {pharmacy.phone_number}")
                        phone_number = input() or pharmacy.phone_number
                        pharmacy.name = name
                        pharmacy.address = address
                        pharmacy.phone_number = phone_number
                        pharmacy.save()
                        print("Pharmacy saved!")
                        self.display()
                    elif choice == 4:
                        print("Let's delete a pharmacy!")
                        print("Enter the pharmacy's id: ")
                        pharmacy_id = int(input())
                        pharmacy = models.pharmacies.Pharmacy(id=pharmacy_id).get(
                            pharmacy_id
                        )
                        pharmacy.delete()
                        print("Pharmacy deleted!")
                        self.display()
                    elif choice == 5:
                        break
                    else:
                        print("That's not a valid choice!")
                        self.display()
                except ValueError:
                    print("That's not a valid choice!")
                    self.display()
        except KeyboardInterrupt:
            print("Goodbye!")
            exit()
