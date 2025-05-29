from sqlalchemy.orm import sessionmaker
from models.db_models import Sample, CBCResult, AnalysisLog
from database.setup import get_engine
from datetime import datetime

#create a session
engine = get_engine()
Session = sessionmaker(bind= engine)
session = Session()

#sample
sample = Sample(
    sample_id = "DG-001",
    patient_name = "Kasongo",
    date_collection  = datetime.utcnow()
)

# Sample CBC results with normal ranges and values
cbc_tests = [
    {"test_name": "WBC", "value": 3.2,"Units":"x10^9/l", "normal_min": 4.0, "normal_max": 11.0},
    {"test_name": "RBC", "value": 5.1, "Units":"x10^12/l","normal_min": 4.7, "normal_max": 6.1},
    {"test_name": "Hemoglobin", "value": 14.5,"Units":"g/dl", "normal_min": 13.0, "normal_max": 17.0},
    {"test_name": "Platelets", "value": 220, "Units":"x10^9/l","normal_min": 150, "normal_max": 400},
    {"test_name": "Hematocrit", "value": 44,"Units":"percent", "normal_min": 44, "normal_max": 50},
    {"test_name": "MCV(mean cell volume)", "Units":"fl","value":88 , "normal_min":80 , "normal_max":100 },
    {"test_name": "MCH(mean cell haemologin)","Units":"pg", "value": 29.6, "normal_min":27 , "normal_max": 33},
    {"test_name": "MCHC(mean cell haemoglobin conc.)","Units":"g/dl", "value":33.6 , "normal_min": 32, "normal_max": 36}

]