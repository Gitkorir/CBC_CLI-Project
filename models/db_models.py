from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Float
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

class CBCResult(Base):
    __tablename__ = 'cbc_results'

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey('samples.id'))
    test_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(String, nullable=True)
    normal_min = Column(Float, nullable=False)
    normal_max = Column(Float, nullable=False)
    flag = Column(String)  # 'Low', 'Normal', 'High'

    sample = relationship("Sample", back_populates="cbc_results", cascade="all, delete")

class AnalysisLog(Base):
    __tablename__ = 'analysis_logs'

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey('samples.id'))
    action = Column(String)  # e.g., "Loaded from CSV", "Analyzed", "Flagged"
    timestamp = Column(DateTime, default=datetime.utcnow)

    sample = relationship("Sample", back_populates="logs")

    def __repr__(self):
        return f"<AnalysisLog(action='{self.action}', timestamp={self.timestamp})>"    
    
class CBCTest(Base):
    __tablename__ = 'cbctests'

    id = Column(Integer, primary_key=True)
    test_name = Column(String, unique=True, nullable=False)
    units = Column(String, nullable=True)
    normal_min = Column(Float, nullable=True)
    normal_max = Column(Float, nullable=True)

    def __repr__(self):
        return f"<CBCTest(name={self.test_name}, units={self.units}, range={self.normal_min}-{self.normal_max})>"    