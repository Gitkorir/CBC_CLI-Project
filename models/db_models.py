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

    cbc_results = relationship("CBCResult", back_populates="sample", cascade="all, delete-orphan")
    logs = relationship("AnalysisLog", back_populates="sample", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sample(id={self.id}, sample_id='{self.sample_id}', patient_name='{self.patient_name}')>"
    
class AnalysisLog(Base):
    __tablename__ = 'analysis_logs'

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey('samples.id'))
    action = Column(String)  # e.g., "Loaded from CSV", "Analyzed", "Flagged"
    timestamp = Column(DateTime, default=datetime.utcnow)

    sample = relationship("Sample", back_populates="logs")

    def __repr__(self):
        return f"<AnalysisLog(action='{self.action}', timestamp={self.timestamp})>"    