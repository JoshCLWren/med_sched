CREATE TABLE IF NOT EXISTS patients(id, first_name, last_name, birth_date);
CREATE TABLE IF NOT EXISTS pharmacies(id, name, address, city, state, zip_code, phone_number, fax_number, email, website, is_default, created_at, updated_at);
CREATE TABLE IF NOT EXISTS prescriptions(id, name, dosage, notes, morning_tablets, afternoon_tablets, evening_tablets, refills, refill_expiration_date, rx_number, owner_id, current_inventory);
CREATE TABLE IF NOT EXISTS schedules(id, patient_id, afternoon_medication, evening_medication, morning_medication, created_at, updated_at);