from sqlalchemy.orm import sessionmaker
from database.setup import get_engine
from models.db_models import Base

engine = get_engine() 
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
