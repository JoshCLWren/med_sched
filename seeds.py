import json
import random

from faker import Faker

import models


def create_seed_data():
    """Either use Faker to create fake json or use existing db values to create json seed file"""

    print("Would you like to use Faker to create fake data? (y/n)")
    if input() == "y":
        print("Creating fake data...")
        fake = Faker()
        patients = []
        prescriptions = []
        schedules = []
        pharmacies = []
        for _ in range(10):
            patient = {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "birth_date": fake.date(),
                "id": random.randint(1, 100),
            }
            patients.append(patient)
            prescription = {
                "name": fake.name(),
                "dosage": f"{random.randint(1, 10)}mg",
                "notes": fake.text(),
                "morning_tablets": random.randint(1, 10),
                "afternoon_tablets": random.randint(1, 10),
                "evening_tablets": random.randint(1, 10),
                "refills": random.randint(1, 10),
                "refill_expiration_date": fake.date(),
                "rx_number": random.randint(100000, 999999),
                "owner_id": random.randint(1, 10),
                "id": random.randint(10000, 99999),
                "current_inventory": random.randint(1, 100),
            }
            prescriptions.append(prescription)
            morning_medication = []
            afternoon_medication = []
            evening_medication = []
            if random.randint(0, 1):
                morning_medication.append(
                    {prescription["name"]: prescription["morning_tablets"]}
                )
            if random.randint(0, 1):
                afternoon_medication.append(
                    {prescription["name"]: prescription["afternoon_tablets"]}
                )
            if random.randint(0, 1):
                evening_medication.append(
                    {prescription["name"]: prescription["evening_tablets"]}
                )
            schedule = {
                "morning_medication": morning_medication,
                "afternoon_medication": afternoon_medication,
                "evening_medication": evening_medication,
                "patient_id": patient["id"],
                "id": random.randint(10000, 99999),
            }
            schedules.append(schedule)

            pharmacy = {
                "name": fake.name(),
                "address": fake.address(),
                "city": fake.city(),
                "state": fake.state(),
                "zip_code": fake.zipcode(),
                "phone_number": fake.phone_number(),
                "fax_number": fake.phone_number(),
                "email": fake.email(),
                "website": fake.url(),
                "is_default": random.randint(0, 1),
                "created_at": fake.date(),
                "updated_at": fake.date(),
                "id": random.randint(10000, 99999),
            }
            pharmacies.append(pharmacy)
        data = {
            "patients": patients,
            "prescriptions": prescriptions,
            "schedules": schedules,
            "pharmacies": pharmacies,
        }
        with open("seeds.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Fake data created!")

    else:
        # get data from database
        print("Getting data from database...")
        all_data = []
        for entity in ("patients", "prescriptions", "schedules", "pharmacies"):
            print(f"Getting all {entity}... from the database")
            try:
                all_data.append(models.get_all(entity))
            except Exception as e:
                print(f"Error getting {entity} from database!")
                print(e)
                return
        if all_data:
            print("Data found, creating json file...")
            data = {
                "patients": all_data[0],
                "prescriptions": all_data[1],
                "schedules": all_data[2],
                "pharmacies": all_data[3],
            }
            with open("seeds.json", "w") as f:
                json.dump(data, f, indent=4)
            print("Json file created!")
        else:
            print("No data found, sorry!")


def load_seeds():
    """Iterate over json data and add to database"""
    print("Finding seed data...")
    try:
        with open("seeds.json") as f:
            data = json.load(f)
        print("Seed data found!")
        for patient in data["patients"]:
            patient = models.patients.Patient(**patient)
            try:
                patient.save()
                print(
                    f"Patient {patient.first_name} {patient.last_name} added to database!"
                )
            except Exception as e:
                print("There was an error adding the patient to the database!")
                print(e)
        for prescription in data["prescriptions"]:
            prescription = models.prescriptions.Prescription(**prescription)
            try:
                prescription.save()
                print(f"Prescription {prescription.name} added to database!")
            except Exception as e:
                print("There was an error adding the prescription to the database!")
                print(e)
        for schedule in data["schedules"]:
            schedule = models.schedules.Schedule(**schedule)
            try:
                schedule.save()
                print(f"Schedule {schedule.id} added to database!")
            except Exception as e:
                print("There was an error adding the schedule to the database!")
                print(e)
        for pharmacy in data["pharmacies"]:
            pharmacy = models.pharmacies.Pharmacy(**pharmacy)
            try:
                pharmacy.save()
                print(f"Pharmacy {pharmacy.name} added to database!")
            except Exception as e:
                print("There was an error adding the pharmacy to the database!")
                print(e)
    except FileNotFoundError:
        print("No seeds.json file found.")
        print("Would you like to create one? (y/n)")
        if input() == "y":
            create_seed_data()
            load_seeds()
        else:
            print("No seed file created.")
            return
    except Exception as e:
        print("There was an error loading the seed data!")
        print(e)
