from sqlalchemy import Column, Integer, Date, Numeric, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ahorro(Base):
    __tablename__ = 'Ahorro'
    ID_Ahorro = Column(Integer, primary_key=True, autoincrement=True)
    Fecha = Column(Date)
    Ingreso = Column(Numeric(precision=8, scale=2))
    Gasto = Column(Numeric(precision=8, scale=2))

class Plan(Base):
    __tablename__ = 'Plan'
    ID_Plan = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(VARCHAR(50))
    Budget = Column(Integer)
                   