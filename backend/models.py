from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    merchant = Column(String)
    credit_card_number = Column(String)
    timestamp = Column(DateTime)
    is_fraudulent = Column(Boolean, default=False)

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    condition = Column(String)
    action = Column(String)