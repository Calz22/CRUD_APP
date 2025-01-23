from sqlalchemy import Column, Integer, String
from database import Base

class Mahasiswa(Base):
    __tablename__ = 'mahasiswa'
    id = Column(Integer, primary_key=True)
    nim = Column(String(10), unique=True)
    nama = Column(String(100))
    jurusan = Column(String(50))