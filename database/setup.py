import os
from sqlalchemy import create_engine
from models.db_models import Base

#define the db file path
DB_FILENAME = "cbc_analysis.db"

def get_engine():
    #craete an SQLite engine
    return create_engine(f"sqlite:///{DB_FILENAME}")

def initialize_database():
    engine = get_engine()

    #create all table from Base's metadata
    Base.metadata.create_all(engine)
    print(f"Database '{DB_FILENAME}' initialized successfully.")

if __name__ == "__main__":
    initialize_database()   