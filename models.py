from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
import json
from flask import Flask
from config import *

def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

class Device(db.Model):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    creationdate = Column(DateTime, nullable=False)
    lastupdate = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False, default=False)
    def __init__(self, DeviceName, CreationDate, LatestUpdate, Status):
        self.name = DeviceName
        self.creationdate = CreationDate
        self.lastupdate = LatestUpdate
        self.status = Status

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "ID": self.id,
            "DeviceName": self.name,
            "CreationDate": self.creationdate,
            "LatestUpdate": self.lastupdate,
            "Status": self.status
        }

class Measures(db.Model):
    __tablename__ = "measures"
    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Float, nullable=False, default = 0.0)
    rank = Column(Integer, nullable=False, default = 0)
    time = Column(DateTime, nullable=False)
    deviceid = Column(Integer, nullable=False)

    def __init__(self, Value, Rank, DeviceId, DateTime):
        self.value = Value
        self.rank = Rank
        self.time = DateTime
        self.deviceid = DeviceId

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "ID": self.id,
            "Value": self.value,
            "time": self.time,
            "Rank": self.rank,
            "DeviceId": self.deviceid
        }