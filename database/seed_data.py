from sqlalchemy.orm import sessionmaker
from models.db_models import Sample, CBCResult, AnalysisLog
from database.setup import get_engine
from datetime import datetime

#create a session
engine = get_engine()
Session = sessionmaker(bind= engine)
session = Session()