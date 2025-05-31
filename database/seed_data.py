from sqlalchemy.orm import sessionmaker
from models.db_models import Sample, CBCResult, AnalysisLog,CBCTest
from database.setup import get_engine
from datetime import datetime
from models.db_models import CBCTest

# Create a session
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()
print("Engine URL:", engine.url)

# Reference test data
reference_tests = [
    {"test_name": "WBC", "units": "x10^9/l", "normal_min": 4.0, "normal_max": 11.0},
    {"test_name": "RBC", "units": "x10^12/l", "normal_min": 4.7, "normal_max": 6.1},
    {"test_name": "Hemoglobin", "units": "g/dl", "normal_min": 13.0, "normal_max": 17.0},
    {"test_name": "Platelets", "units": "x10^9/l", "normal_min": 150, "normal_max": 400},
    {"test_name": "Hematocrit", "units": "percent", "normal_min": 44, "normal_max": 50},
    {"test_name": "MCV", "units": "fl", "normal_min": 80, "normal_max": 100},
    {"test_name": "MCH", "units": "pg", "normal_min": 27, "normal_max": 33},
    {"test_name": "MCHC", "units": "g/dl", "normal_min": 32, "normal_max": 36}
]

for ref in reference_tests:
    exists = session.query(CBCTest).filter_by(test_name=ref["test_name"]).first()
    if not exists:
        session.add(CBCTest(**ref))
session.commit()
print("✅ Reference CBC test data seeded.")


# Check if the sample already exists
existing = session.query(Sample).filter_by(sample_id="DG-001").first()

if not existing:
    # Sample
    sample = Sample(
        sample_id="DG-001",
        patient_name="Kasongo",
        date_collected=datetime.utcnow()
    )

    # CBC results test-values
    test_values = {
    "WBC": 3.2,
    "RBC": 5.1,
    "Hemoglobin": 14.5,
    "Platelets": 220,
    "Hematocrit": 44,
    "MCV": 88,
    "MCH": 29.6,
    "MCHC": 33.6
}



    # Add CBC results and determine flags
    for test_name, value in test_values.items():
        ref = session.query(CBCTest).filter_by(test_name=test_name).first()
        if not ref:
            print(f"⚠️ Reference test for '{test_name}' not found. Skipping.")
            continue

        if value < ref.normal_min:
            flag = "Low"
        elif value > ref.normal_max:
            flag = "High"
        else:
            flag = "Normal"

        result = CBCResult(
            test_name=test_name,
            value=value,
            units=ref.units,
            normal_min=ref.normal_min,
            normal_max=ref.normal_max,
            flag=flag
        )
        sample.cbc_results.append(result)

    # Add analysis log
    log = AnalysisLog(action="Insert test CBC data", timestamp=datetime.utcnow())
    sample.logs.append(log)

    # Commit
    session.add(sample)
    session.commit()
    print("\u2705 Sample data inserted successfully!")

else:
    print("\u26A0\uFE0F Sample with ID 'DG-001' already exists. Skipping insert.")
