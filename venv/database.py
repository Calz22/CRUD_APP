from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Konfigurasi database
DATABASE_URL = 'mysql+pymysql://root@localhost/db_mahasiswa'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
db_session = scoped_session(SessionLocal)