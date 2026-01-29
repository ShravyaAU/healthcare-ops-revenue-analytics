# scripts/generate_healthcare_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

# Settings
OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)
random.seed(42)

NUM_APPOINTMENTS = 5000
START_DATE = datetime(2024, 1, 1)  # one year of data

departments = ["Cardiology", "Orthopedics", "Neurology", "General Medicine", "Pediatrics"]
providers = [f"P{str(i).zfill(3)}" for i in range(1, 51)]
payers = ["Medicare", "Medicaid", "Blue Cross", "Aetna", "United", "Self-Pay"]
appointment_statuses = ["Completed", "No-show", "Cancelled"]
claim_statuses = ["Paid", "Denied", "Pending"]

# -----------------------
# Generate Appointments
# -----------------------
appointments = []
for i in range(NUM_APPOINTMENTS):
    appointment_date = START_DATE + timedelta(days=random.randint(0, 365))
    status = random.choices(appointment_statuses, weights=[0.75, 0.15, 0.10], k=1)[0]
    appointments.append({
        "appointment_id": f"A{str(i).zfill(6)}",
        "patient_id": f"PT{random.randint(1000, 9999)}",
        "provider_id": random.choice(providers),
        "department": random.choice(departments),
        "appointment_date": appointment_date.strftime("%Y-%m-%d"),
        "appointment_status": status
    })
appointments_df = pd.DataFrame(appointments)

# -----------------------
# Generate Claims
# -----------------------
claims = []
claim_seq = 100000
for _, row in appointments_df.iterrows():
    if row["appointment_status"] != "Completed":
        continue  # only completed visits generate claims

    claim_amount = round(random.uniform(100, 5000), 2)
    status = random.choices(claim_statuses, weights=[0.7, 0.2, 0.1], k=1)[0]

    paid_amount = round(claim_amount * random.uniform(0.6, 1.0), 2) if status == "Paid" else 0.0
    payment_date = (datetime.strptime(row["appointment_date"], "%Y-%m-%d") + timedelta(days=random.randint(15, 120))).strftime("%Y-%m-%d") if status == "Paid" else ""

    claims.append({
        "claim_id": f"C{claim_seq}",
        "appointment_id": row["appointment_id"],
        "patient_id": row["patient_id"],
        "payer": random.choice(payers),
        "claim_amount": claim_amount,
        "paid_amount": paid_amount,
        "claim_status": status,
        "payment_date": payment_date
    })
    claim_seq += 1

claims_df = pd.DataFrame(claims)

# -----------------------
# Save raw files
# -----------------------
appointments_path = OUT_DIR / "appointments.csv"
claims_path = OUT_DIR / "claims.csv"

appointments_df.to_csv(appointments_path, index=False)
claims_df.to_csv(claims_path, index=False)

print("Generated:")
print(f"- appointments: {len(appointments_df)} rows -> {appointments_path}")
print(f"- claims:       {len(claims_df)} rows -> {claims_path}")
