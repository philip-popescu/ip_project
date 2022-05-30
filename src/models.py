from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()


class Client(db.Model):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    nume = Column(String(50))
    telefon = Column(String(12))
    email = Column(String(50), unique=True)
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


class Locatie(db.Model):
    __tablename__ = 'locatie'
    id = Column(Integer, primary_key=True)
    address = Column(String(80))
    cost_md = Column(Float)
    coat_P = Column(Float)
    tip = Column(String(20))
    description = Column(String(200))


class Angajat(db.Model):
    __tablename__ = 'angajat'
    id = Column(Integer, primary_key=True)
    nume = Column(String(50))
    prenume = Column(String(50))
    password = Column(String(50))
    telefon = Column(String(12))
    email = Column(String(50))
    post = Column(String(10))
    lid = Column(Integer, ForeignKey("locatie.id", ondelete="CASCADE"))


class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    nr_paturi = Column(Integer)
    etaj = Column(Integer)
    numar = Column(Integer)
    lid = Column(Integer, ForeignKey("locatie.id", ondelete="CASCADE"))


class Rezervare(db.Model):
    __tablename__ = 'rezervare'
    id = Column(Integer, primary_key=True)
    lid = Column(Integer, ForeignKey("locatie.id", ondelete="CASCADE"))
    cpid = Column(Integer, ForeignKey("c_p.id", ondelete="CASCADE"))
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    total_plata = Column(Float)
    status = Column(Integer)
    mic_dejun = Column(Boolean)
    reducere = Column(Float())
    data_r = Column(DateTime)


class RR(db.Model):
    __tablename__ = 'r_r'
    id = Column(Integer, ForeignKey('rezervare.id', ondelete='CASCADE'), primary_key=True)
    rid = Column(Integer, ForeignKey('room.id', ondelete='CASCADE'), primary_key=True)


class Reducere(db.Model):
    __tablename__ = 'reducere'
    id = Column(Integer, primary_key=True)
    lid = Column(Integer, ForeignKey("locatie.id", ondelete="DELETE"))
    from_date = Column(DateTime)
    to_date = Column(DateTime)

