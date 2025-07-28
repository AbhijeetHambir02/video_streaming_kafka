from sqlalchemy import Column, Integer, String, DateTime
from app.utils import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

class StoreFile(Base):
    __tablename__ = 'video_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(100), nullable=False, unique=True)
    file_name = Column(String(100), nullable=False)
    file_path = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
