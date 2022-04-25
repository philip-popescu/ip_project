from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, validates

# declarative base class
Base = declarative_base()


class Client(db.Model):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    nume = Column(String(50))
    telefon = Column(String(10))
    email = Column(String(50))
    password = Column(String(50))

    def __str__(self):
        return self.nume


class MetodaPlata(db.Model):
    __tablename__ = 'metoda_plata'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    expiration = Column(DateTime)
