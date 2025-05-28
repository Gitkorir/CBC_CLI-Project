from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Sample(Base):

    __tablename__ = "samples"

    id = Column(Integer, primary_key=True)
    sample_id =Column(String,unique=True)
    patient_name = Column(String)
    date_collected = Column(DateTime, default=datetime.utcnow)