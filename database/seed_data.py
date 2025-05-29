from sqlalchemy.orm import sessionmaker
from models.db_models import Sample, CBCResult, AnalysisLog
from database.setup import get_engine
from datetime import datetime

# Create a session
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()
print("Engine URL:", engine.url)


# Check if the sample already exists
existing = session.query(Sample).filter_by(sample_id="DG-001").first()

if not existing:
    # Sample
    sample = Sample(
        sample_id="DG-001",
        patient_name="Kasongo",
        date_collected=datetime.utcnow()
    )

    # CBC results
    cbc_tests = [
        {"test_name": "WBC", "value": 3.2, "Units": "x10^9/l", "normal_min": 4.0, "normal_max": 11.0},
        {"test_name": "RBC", "value": 5.1, "Units": "x10^12/l", "normal_min": 4.7, "normal_max": 6.1},
        {"test_name": "Hemoglobin", "value": 14.5, "Units": "g/dl", "normal_min": 13.0, "normal_max": 17.0},
        {"test_name": "Platelets", "value": 220, "Units": "x10^9/l", "normal_min": 150, "normal_max": 400},
        {"test_name": "Hematocrit", "value": 44, "Units": "percent", "normal_min": 44, "normal_max": 50},
        {"test_name": "MCV(mean cell volume)", "value": 88, "Units": "fl", "normal_min": 80, "normal_max": 100},
        {"test_name": "MCH(mean cell haemologin)", "value": 29.6, "Units": "pg", "normal_min": 27, "normal_max": 33},
        {"test_name": "MCHC(mean cell haemoglobin conc.)", "value": 33.6, "Units": "g/dl", "normal_min": 32, "normal_max": 36}
    ]

    # Add CBC results and determine flags
    for test in cbc_tests:
        value = test["value"]
        if value < test["normal_min"]:
            flag = "Low"
        elif value > test["normal_max"]:
            flag = "High"
        else:
            flag = "Normal"

        result = CBCResult(
            test_name=test["test_name"],
            value=value,
            normal_min=test["normal_min"],
            normal_max=test["normal_max"],
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
