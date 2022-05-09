from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
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
    cod = Column(String(16))
    cvv = Column(String(3))


class CP(db.Model):
    __tablename__ = 'c_p'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey("metoda_plata.id", ondelete="CASCADE"))
    cid = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    saved = Column(Boolean)




